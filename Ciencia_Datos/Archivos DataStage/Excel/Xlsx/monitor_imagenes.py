"""
Monitor de Imágenes - Tabla [tru].[Formulario]
Descarga automáticamente imágenes nuevas de la columna [Imagen_Dos]
"""

import io
import os
import json
import time
import requests
import pyodbc
from datetime import datetime
from urllib.parse import urlparse
from PIL import Image

# --- Configuración ---
CARPETA_DESTINO    = r"C:\Users\analistabi\Downloads\ImagenPrueba"
ARCHIVO_ESTADO     = os.path.join(os.path.dirname(__file__), "imagenes_descargadas.json")
INTERVALO_SEGUNDOS = 30   # cada cuántos segundos se consulta la tabla

CONN_STRING = (
    "DRIVER={SQL Server};"
    "SERVER=192.168.0.133;"
    "DATABASE=DataLake;"
    "UID=siesarayo;"
    "PWD=SisR@yos.2017;"
    "Connection Timeout=30;"
)


# ─────────────────────────────────────────────
#  Base de datos
# ─────────────────────────────────────────────

def conectar():
    return pyodbc.connect(CONN_STRING)


def obtener_urls(conn) -> set:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT [Imagen_Dos]
        FROM   [tru].[Formulario]
        WHERE  [Imagen_Dos] IS NOT NULL
          AND  LTRIM(RTRIM([Imagen_Dos])) <> ''
    """)
    return {row[0].strip() for row in cursor.fetchall()}


# ─────────────────────────────────────────────
#  Estado persistente (JSON local)
# ─────────────────────────────────────────────

def cargar_estado() -> set:
    if os.path.exists(ARCHIVO_ESTADO):
        with open(ARCHIVO_ESTADO, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def guardar_estado(urls: set):
    with open(ARCHIVO_ESTADO, "w", encoding="utf-8") as f:
        json.dump(sorted(urls), f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────
#  Descarga
# ─────────────────────────────────────────────

def _nombre_base(url: str) -> str:
    base = os.path.splitext(os.path.basename(urlparse(url).path))[0]
    return base if base else f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def descargar(url: str, carpeta: str) -> bool:
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()

        img = Image.open(io.BytesIO(resp.content))
        ext = ".png" if (img.format or "") == "PNG" else ".jpg"

        base  = _nombre_base(url)
        ruta  = os.path.join(carpeta, base + ext)
        if os.path.exists(ruta):
            ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
            ruta = os.path.join(carpeta, f"{base}_{ts}{ext}")

        if ext == ".jpg" and img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        img.save(ruta)
        print(f"  [OK] {os.path.basename(ruta)}")
        return True

    except Exception as e:
        print(f"  [ERROR] {url}\n         {e}")
        return False


# ─────────────────────────────────────────────
#  Bucle principal
# ─────────────────────────────────────────────

def monitorear():
    os.makedirs(CARPETA_DESTINO, exist_ok=True)

    descargadas = cargar_estado()

    print("=" * 55)
    print("  Monitor Imagen_Dos  |  [tru].[Formulario]")
    print("=" * 55)
    print(f"  Destino  : {CARPETA_DESTINO}")
    print(f"  Intervalo: {INTERVALO_SEGUNDOS} s")
    print(f"  Ya registradas: {len(descargadas)} URLs")
    print("-" * 55)

    while True:
        try:
            conn = conectar()
            actuales = obtener_urls(conn)
            conn.close()

            nuevas = actuales - descargadas

            if nuevas:
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n[{ts}]  {len(nuevas)} nueva(s) URL(s) detectada(s):")
                for url in sorted(nuevas):
                    if descargar(url, CARPETA_DESTINO):
                        descargadas.add(url)
                guardar_estado(descargadas)
            else:
                ts = datetime.now().strftime("%H:%M:%S")
                print(f"[{ts}]  Sin cambios...       ", end="\r")

        except pyodbc.Error as e:
            print(f"\n[BD ERROR]  {e}")
        except Exception as e:
            print(f"\n[ERROR]     {e}")

        time.sleep(INTERVALO_SEGUNDOS)


if __name__ == "__main__":
    monitorear()
