"""
Aplicación para cargar archivos (Excel/CSV) e insertarlos en SQL Server.
pip install pandas openpyxl sqlalchemy pyodbc
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import pandas as pd
import urllib.parse
from sqlalchemy import create_engine, text
import os


# ── Valores por defecto ──────────────────────────────────────────────────────
DEFAULTS = {
    "server":   "192.168.0.22",
    "database": "Replica",
    "schema":   "clf",
    "username": "siesarayo",
    "password": "SisR@yos.2017",
}


# ── Lógica de negocio ────────────────────────────────────────────────────────

def read_file(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(path)
    if ext == ".csv":
        # Intenta detectar el separador automáticamente
        return pd.read_csv(path, sep=None, engine="python", encoding="utf-8-sig")
    raise ValueError(f"Formato no soportado: {ext}. Use .xlsx, .xls o .csv")


def build_engine(server, database, username, password):
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password}"
    )
    quoted = urllib.parse.quote_plus(conn_str)
    return create_engine(f"mssql+pyodbc:///?odbc_connect={quoted}", fast_executemany=True)


def insert_dataframe(df, engine, schema, table, if_exists):
    df.to_sql(
        name=table,
        con=engine,
        schema=schema if schema.strip() else None,
        if_exists=if_exists,
        index=False,
        chunksize=1000,
    )


# ── Ventana principal ────────────────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inserción de Archivos → SQL Server")
        self.resizable(False, False)
        self._df: pd.DataFrame | None = None
        self._build_ui()

    # ── Construcción UI ──────────────────────────────────────────────────────

    def _build_ui(self):
        pad = {"padx": 8, "pady": 4}

        # ── Sección: Archivo ─────────────────────────────────────────────────
        frm_file = ttk.LabelFrame(self, text=" 1. Archivo de origen ")
        frm_file.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 4))

        self.var_path = tk.StringVar()
        ttk.Entry(frm_file, textvariable=self.var_path, width=60).grid(
            row=0, column=0, **pad)
        ttk.Button(frm_file, text="Examinar…", command=self._browse).grid(
            row=0, column=1, **pad)
        ttk.Button(frm_file, text="Vista previa", command=self._preview).grid(
            row=0, column=2, **pad)

        self.lbl_info = ttk.Label(frm_file, text="", foreground="gray")
        self.lbl_info.grid(row=1, column=0, columnspan=3, sticky="w", padx=8)

        # ── Sección: Conexión ────────────────────────────────────────────────
        frm_conn = ttk.LabelFrame(self, text=" 2. Conexión a SQL Server ")
        frm_conn.grid(row=1, column=0, sticky="ew", padx=12, pady=4)

        fields = [
            ("Servidor:",  "var_server",   DEFAULTS["server"]),
            ("Base de datos:", "var_db",   DEFAULTS["database"]),
            ("Usuario:",   "var_user",     DEFAULTS["username"]),
            ("Contraseña:", "var_pwd",     DEFAULTS["password"]),
        ]
        for i, (label, attr, default) in enumerate(fields):
            ttk.Label(frm_conn, text=label).grid(row=i, column=0, sticky="e", **pad)
            var = tk.StringVar(value=default)
            setattr(self, attr, var)
            show = "*" if "pwd" in attr else ""
            ttk.Entry(frm_conn, textvariable=var, width=35, show=show).grid(
                row=i, column=1, sticky="w", **pad)

        ttk.Button(frm_conn, text="Probar conexión", command=self._test_conn).grid(
            row=len(fields), column=0, columnspan=2, pady=4)

        # ── Sección: Destino ─────────────────────────────────────────────────
        frm_dest = ttk.LabelFrame(self, text=" 3. Tabla de destino ")
        frm_dest.grid(row=2, column=0, sticky="ew", padx=12, pady=4)

        ttk.Label(frm_dest, text="Esquema:").grid(row=0, column=0, sticky="e", **pad)
        self.var_schema = tk.StringVar(value=DEFAULTS["schema"])
        ttk.Entry(frm_dest, textvariable=self.var_schema, width=20).grid(
            row=0, column=1, sticky="w", **pad)

        ttk.Label(frm_dest, text="Tabla:").grid(row=0, column=2, sticky="e", **pad)
        self.var_table = tk.StringVar()
        ttk.Entry(frm_dest, textvariable=self.var_table, width=30).grid(
            row=0, column=3, sticky="w", **pad)

        ttk.Label(frm_dest, text="Si la tabla existe:").grid(
            row=1, column=0, columnspan=2, sticky="e", **pad)
        self.var_ifexists = tk.StringVar(value="replace")
        for i, opt in enumerate(("replace", "append", "fail")):
            ttk.Radiobutton(
                frm_dest, text=opt.capitalize(), variable=self.var_ifexists, value=opt
            ).grid(row=1, column=2 + i, sticky="w", padx=2)

        # ── Sección: Acción ──────────────────────────────────────────────────
        frm_act = ttk.Frame(self)
        frm_act.grid(row=3, column=0, pady=8)

        self.btn_load = ttk.Button(
            frm_act, text="Cargar a base de datos", command=self._start_load,
            style="Accent.TButton"
        )
        self.btn_load.grid(row=0, column=0, padx=8)

        self.progress = ttk.Progressbar(frm_act, mode="indeterminate", length=200)
        self.progress.grid(row=0, column=1, padx=8)

        self.lbl_status = ttk.Label(self, text="Listo.", foreground="gray")
        self.lbl_status.grid(row=4, column=0, sticky="w", padx=12, pady=(0, 10))

    # ── Acciones ─────────────────────────────────────────────────────────────

    def _browse(self):
        path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[
                ("Todos los soportados", "*.xlsx *.xls *.csv"),
                ("Excel", "*.xlsx *.xls"),
                ("CSV", "*.csv"),
            ],
        )
        if not path:
            return
        self.var_path.set(path)
        # Sugerir nombre de tabla basado en el archivo
        name = os.path.splitext(os.path.basename(path))[0]
        name = name.replace(" ", "_")
        self.var_table.set(name)
        self._load_preview(path)

    def _load_preview(self, path):
        try:
            self._df = read_file(path)
            rows, cols = self._df.shape
            self.lbl_info.config(
                text=f"{rows:,} filas × {cols} columnas  |  "
                     f"Columnas: {', '.join(self._df.columns[:6])}{'…' if cols > 6 else ''}",
                foreground="#555"
            )
        except Exception as e:
            self._df = None
            self.lbl_info.config(text=f"Error al leer: {e}", foreground="red")

    def _preview(self):
        if self._df is None:
            path = self.var_path.get().strip()
            if not path:
                messagebox.showwarning("Sin archivo", "Seleccione un archivo primero.")
                return
            self._load_preview(path)
        if self._df is None:
            return
        PreviewWindow(self, self._df)

    def _test_conn(self):
        self._set_status("Probando conexión…")
        def run():
            try:
                engine = build_engine(
                    self.var_server.get(), self.var_db.get(),
                    self.var_user.get(), self.var_pwd.get()
                )
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                self._set_status("Conexión exitosa.", color="green")
            except Exception as e:
                self._set_status(f"Error de conexión: {e}", color="red")
        threading.Thread(target=run, daemon=True).start()

    def _start_load(self):
        if self._df is None:
            path = self.var_path.get().strip()
            if not path:
                messagebox.showwarning("Sin archivo", "Seleccione un archivo primero.")
                return
            self._load_preview(path)
        if self._df is None:
            return
        table = self.var_table.get().strip()
        if not table:
            messagebox.showwarning("Sin tabla", "Ingrese un nombre de tabla.")
            return

        self.btn_load.config(state="disabled")
        self.progress.start(10)
        self._set_status("Insertando datos…")

        def run():
            try:
                engine = build_engine(
                    self.var_server.get(), self.var_db.get(),
                    self.var_user.get(), self.var_pwd.get()
                )
                insert_dataframe(
                    self._df, engine,
                    self.var_schema.get().strip(),
                    table,
                    self.var_ifexists.get()
                )
                rows = len(self._df)
                db = self.var_db.get()
                schema = self.var_schema.get().strip()
                dest = f"{db}.{schema}.{table}" if schema else f"{db}.{table}"
                self._set_status(
                    f"Éxito: {rows:,} filas insertadas en {dest}", color="green"
                )
            except Exception as e:
                self._set_status(f"Error: {e}", color="red")
                messagebox.showerror("Error al insertar", str(e))
            finally:
                self.progress.stop()
                self.btn_load.config(state="normal")

        threading.Thread(target=run, daemon=True).start()

    def _set_status(self, msg, color="gray"):
        self.lbl_status.config(text=msg, foreground=color)


# ── Ventana de vista previa ──────────────────────────────────────────────────

class PreviewWindow(tk.Toplevel):
    MAX_ROWS = 200

    def __init__(self, parent, df: pd.DataFrame):
        super().__init__(parent)
        self.title("Vista previa")
        self.geometry("900x400")

        sample = df.head(self.MAX_ROWS)
        cols = list(sample.columns)

        tree = ttk.Treeview(self, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=max(80, min(200, len(str(col)) * 9)), anchor="w")

        for _, row in sample.iterrows():
            tree.insert("", "end", values=[str(v) for v in row])

        vsb = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(self, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        total = len(df)
        shown = len(sample)
        note = f"Mostrando {shown} de {total} filas" if total > shown else f"{total} filas"
        ttk.Label(self, text=note, foreground="gray").grid(
            row=2, column=0, sticky="w", padx=6, pady=4)


# ── Punto de entrada ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()
