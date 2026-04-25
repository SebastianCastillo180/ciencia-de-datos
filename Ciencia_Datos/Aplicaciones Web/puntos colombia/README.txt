═══════════════════════════════════════════════════════════════
  FORMULARIO RAYOGAS ESP - PUNTOS COLOMBIA
  Aplicación de Escritorio en Python con Tkinter
═══════════════════════════════════════════════════════════════

DESCRIPCIÓN:
  Aplicación de escritorio para gestionar formularios de clientes
  de Puntos Colombia para Rayogas ESP.

REQUISITOS:
  - Python 3.7 o superior
  - Tkinter (generalmente viene incluido con Python)
  - SQLite3 (incluido con Python)

INSTALACIÓN:
  No requiere instalación adicional. Python incluye todas las
  bibliotecas necesarias.

CÓMO EJECUTAR:
  1. Abrir terminal/cmd en esta carpeta
  2. Ejecutar: python rayogas_formulario.py

  O simplemente hacer doble clic en rayogas_formulario.py

USUARIOS DISPONIBLES:
  - admin       | rayogas2026  (Administrador)
  - usuario     | 12345        (Usuario)
  - operador1   | rayogas123   (Operador)
  - operador2   | rayogas456   (Operador)
  - supervisor  | rayogas789   (Supervisor)

CARACTERÍSTICAS:
  ✓ Logo corporativo de Rayogas en la portada
  ✓ Pantalla de login con usuario y contraseña
  ✓ Botón de salida en la ventana de login
  ✓ 5 usuarios disponibles (admin, usuario, operadores, supervisor)
  ✓ Formulario principal con fecha/hora automática
  ✓ Formulario para clientes creados (recompra)
  ✓ Formulario para clientes nuevos
  ✓ Base de datos SQLite para almacenar información
  ✓ Adjuntar archivos de cédula
  ✓ Colores corporativos: Blanco y Azul #009fe3

INSTALACIÓN OPCIONAL (para mejor calidad del logo):
  pip install -r requirements.txt

ESTRUCTURA DE ARCHIVOS:
  rayogas_formulario.py  - Aplicación principal
  rayogas_puntos.db      - Base de datos (se crea automáticamente)
  uploads/               - Carpeta para archivos adjuntos
  README.txt             - Este archivo

BASE DE DATOS:
  La aplicación crea automáticamente una base de datos SQLite
  llamada "rayogas_puntos.db" con dos tablas:

  - clientes_creados: Para clientes que ya existen
  - clientes_nuevos: Para clientes nuevos con toda la información

ARCHIVOS ADJUNTOS:
  Las fotos de cédula se guardan en la carpeta "uploads"
  con el formato: {cedula}_{fecha}_{hora}_{nombre_archivo}

SOPORTE:
  Para problemas o preguntas, contacte al desarrollador.

═══════════════════════════════════════════════════════════════
  Desarrollado con Python y Tkinter
  © 2026 Rayogas ESP
═══════════════════════════════════════════════════════════════
