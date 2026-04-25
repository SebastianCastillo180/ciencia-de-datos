"""
Formulario Rayogas ESP - Puntos Colombia
Aplicación de escritorio para gestión de clientes
Desarrollado en Python con Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import sqlite3
import os
import shutil

try:
    from PIL import Image, ImageTk
    PIL_DISPONIBLE = True
except ImportError:
    PIL_DISPONIBLE = False

# Colores corporativos
COLOR_AZUL = "#009fe3"
COLOR_BLANCO = "#ffffff"
COLOR_GRIS_CLARO = "#f0f0f0"
COLOR_AZUL_OSCURO = "#0077b3"

class BaseDatos:
    """Clase para manejar la base de datos SQLite"""

    def __init__(self):
        self.conn = sqlite3.connect('rayogas_puntos.db')
        self.crear_tablas()

    def crear_tablas(self):
        cursor = self.conn.cursor()

        # Tabla clientes creados
        cursor.execute('''CREATE TABLE IF NOT EXISTS clientes_creados
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          fecha_registro TEXT,
                          nombre_completo TEXT,
                          cedula TEXT,
                          direccion TEXT,
                          zona TEXT,
                          puntos_acumulados INTEGER)''')

        # Tabla clientes nuevos
        cursor.execute('''CREATE TABLE IF NOT EXISTS clientes_nuevos
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          fecha_registro TEXT,
                          nombre_completo TEXT,
                          cedula TEXT,
                          celular TEXT,
                          ciudad TEXT,
                          zona TEXT,
                          direccion TEXT,
                          uso_gas TEXT,
                          inscrito_puntos TEXT,
                          monto_compra REAL,
                          puntos_acumulados INTEGER,
                          autorizacion_datos TEXT,
                          archivo_cedula TEXT)''')

        self.conn.commit()

    def guardar_cliente_creado(self, datos):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO clientes_creados
                         (fecha_registro, nombre_completo, cedula, direccion, zona, puntos_acumulados)
                         VALUES (?, ?, ?, ?, ?, ?)''', datos)
        self.conn.commit()

    def guardar_cliente_nuevo(self, datos):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO clientes_nuevos
                         (fecha_registro, nombre_completo, cedula, celular, ciudad, zona,
                          direccion, uso_gas, inscrito_puntos, monto_compra, puntos_acumulados,
                          autorizacion_datos, archivo_cedula)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', datos)
        self.conn.commit()

    def cerrar(self):
        self.conn.close()


class VentanaLogin:
    """Ventana de inicio de sesión"""

    def __init__(self, root, callback_exito):
        self.root = root
        self.callback_exito = callback_exito

        # Usuarios válidos
        self.usuarios = {
            'admin': 'rayogas2026',
            'usuario': '12345',
            'operador1': 'rayogas123',
            'operador2': 'rayogas456',
            'supervisor': 'rayogas789'
        }

        self.crear_interfaz()

    def crear_interfaz(self):
        # Frame principal
        frame = tk.Frame(self.root, bg=COLOR_BLANCO)
        frame.pack(expand=True, fill='both', padx=50, pady=30)

        # Logo
        try:
            logo_path = os.path.join(os.path.dirname(__file__), 'logo_rayogas.png')
            if PIL_DISPONIBLE:
                # Usar PIL para mejor calidad
                logo_img = Image.open(logo_path)
                logo_img = logo_img.resize((300, 120), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_img)
            else:
                # Usar PhotoImage de Tkinter (sin redimensionamiento)
                logo_photo = tk.PhotoImage(file=logo_path)
                # Redimensionar si es muy grande (subsample)
                logo_photo = logo_photo.subsample(2, 2)

            logo_label = tk.Label(frame, image=logo_photo, bg=COLOR_BLANCO)
            logo_label.image = logo_photo
            logo_label.pack(pady=15)
        except Exception as e:
            # Si no se puede cargar el logo, mostrar texto
            tk.Label(frame, text="RAYOGAS",
                    font=('Arial', 28, 'bold'), fg=COLOR_AZUL, bg=COLOR_BLANCO).pack(pady=10)

        # Encabezado
        tk.Label(frame, text="Formulario Rayogas ESP",
                font=('Arial', 20, 'bold'), fg=COLOR_AZUL, bg=COLOR_BLANCO).pack(pady=5)
        tk.Label(frame, text="Puntos Colombia",
                font=('Arial', 14), fg=COLOR_AZUL_OSCURO, bg=COLOR_BLANCO).pack(pady=5)

        # Separador
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=20)

        # Campo usuario
        tk.Label(frame, text="Usuario:", font=('Arial', 12), bg=COLOR_BLANCO).pack(pady=5)
        self.entry_usuario = tk.Entry(frame, font=('Arial', 12), width=30)
        self.entry_usuario.pack(pady=5)

        # Campo contraseña
        tk.Label(frame, text="Contraseña:", font=('Arial', 12), bg=COLOR_BLANCO).pack(pady=5)
        self.entry_password = tk.Entry(frame, font=('Arial', 12), width=30, show='*')
        self.entry_password.pack(pady=5)

        # Botones
        btn_frame = tk.Frame(frame, bg=COLOR_BLANCO)
        btn_frame.pack(pady=15)

        btn_ingresar = tk.Button(btn_frame, text="Ingresar", font=('Arial', 12, 'bold'),
                                bg=COLOR_AZUL, fg=COLOR_BLANCO, width=15, height=2,
                                cursor='hand2', command=self.validar_login)
        btn_ingresar.pack(side='left', padx=5)

        btn_salir = tk.Button(btn_frame, text="Salir", font=('Arial', 12, 'bold'),
                             bg='#dc3545', fg=COLOR_BLANCO, width=15, height=2,
                             cursor='hand2', command=self.salir)
        btn_salir.pack(side='left', padx=5)

        # Info
        info_frame = tk.Frame(frame, bg=COLOR_GRIS_CLARO, relief='groove', borderwidth=2)
        info_frame.pack(pady=10, fill='x')
        tk.Label(info_frame, text="Usuarios disponibles:", font=('Arial', 10, 'bold'),
                bg=COLOR_GRIS_CLARO, fg=COLOR_AZUL_OSCURO).pack(pady=5)

        usuarios_info = [
            "admin / rayogas2026",
            "usuario / 12345",
            "operador1 / rayogas123",
            "operador2 / rayogas456",
            "supervisor / rayogas789"
        ]

        for usuario_info in usuarios_info:
            tk.Label(info_frame, text=usuario_info, font=('Arial', 8),
                    bg=COLOR_GRIS_CLARO).pack(pady=1)

        # Bind Enter
        self.entry_password.bind('<Return>', lambda e: self.validar_login())

    def salir(self):
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir de la aplicación?"):
            self.root.quit()

    def validar_login(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()

        if usuario in self.usuarios and self.usuarios[usuario] == password:
            self.callback_exito()
        else:
            messagebox.showerror("Error de autenticación",
                               f"Usuario o contraseña incorrectos.\n\n"
                               f"Credenciales válidas:\n"
                               f"• admin / rayogas2026\n"
                               f"• usuario / 12345\n"
                               f"• operador1 / rayogas123\n"
                               f"• operador2 / rayogas456\n"
                               f"• supervisor / rayogas789\n\n"
                               f"Verifique mayúsculas/minúsculas y espacios.")


class VentanaFormularioPrincipal:
    """Ventana del formulario principal"""

    def __init__(self, root, db, callback_cliente_creado, callback_cliente_nuevo):
        self.root = root
        self.db = db
        self.callback_cliente_creado = callback_cliente_creado
        self.callback_cliente_nuevo = callback_cliente_nuevo
        self.fecha_registro = None

        self.crear_interfaz()

    def crear_interfaz(self):
        # Frame principal
        frame = tk.Frame(self.root, bg=COLOR_BLANCO)
        frame.pack(expand=True, fill='both', padx=30, pady=30)

        # Encabezado
        header = tk.Frame(frame, bg=COLOR_AZUL, height=100)
        header.pack(fill='x', pady=(0, 20))
        tk.Label(header, text="Formulario Rayogas ESP",
                font=('Arial', 20, 'bold'), fg=COLOR_BLANCO, bg=COLOR_AZUL).pack(pady=10)
        tk.Label(header, text="Puntos Colombia",
                font=('Arial', 14), fg=COLOR_BLANCO, bg=COLOR_AZUL).pack()

        # Contenido
        contenido = tk.Frame(frame, bg=COLOR_GRIS_CLARO, relief='raised', borderwidth=2)
        contenido.pack(fill='both', expand=True, padx=20, pady=20)

        # Fecha y hora
        tk.Label(contenido, text="Fecha y Hora de Registro:",
                font=('Arial', 12, 'bold'), bg=COLOR_GRIS_CLARO).pack(pady=(20, 5))
        self.label_fecha = tk.Label(contenido, text="", font=('Arial', 12),
                                    bg=COLOR_BLANCO, relief='sunken', width=40)
        self.label_fecha.pack(pady=5)
        self.actualizar_fecha()

        # Pregunta recompra
        tk.Label(contenido, text="¿Es una Recompra?",
                font=('Arial', 12, 'bold'), bg=COLOR_GRIS_CLARO).pack(pady=(30, 10))

        self.var_recompra = tk.StringVar()

        radio_frame = tk.Frame(contenido, bg=COLOR_GRIS_CLARO)
        radio_frame.pack(pady=10)

        tk.Radiobutton(radio_frame, text="SI (Cliente Creado)", variable=self.var_recompra,
                      value="SI", font=('Arial', 11), bg=COLOR_GRIS_CLARO,
                      cursor='hand2').pack(side='left', padx=20)
        tk.Radiobutton(radio_frame, text="NO (Cliente Nuevo)", variable=self.var_recompra,
                      value="NO", font=('Arial', 11), bg=COLOR_GRIS_CLARO,
                      cursor='hand2').pack(side='left', padx=20)

        # Botón continuar
        btn_continuar = tk.Button(contenido, text="Continuar", font=('Arial', 12, 'bold'),
                                 bg=COLOR_AZUL, fg=COLOR_BLANCO, width=25, height=2,
                                 cursor='hand2', command=self.continuar)
        btn_continuar.pack(pady=30)

    def actualizar_fecha(self):
        ahora = datetime.now()
        self.fecha_registro = ahora.strftime('%Y-%m-%d %H:%M:%S')
        self.label_fecha.config(text=ahora.strftime('%d/%m/%Y %H:%M:%S'))
        self.root.after(1000, self.actualizar_fecha)

    def continuar(self):
        if not self.var_recompra.get():
            messagebox.showwarning("Advertencia", "Por favor seleccione una opción")
            return

        if self.var_recompra.get() == "SI":
            self.callback_cliente_creado(self.fecha_registro)
        else:
            self.callback_cliente_nuevo(self.fecha_registro)


class VentanaClienteCreado:
    """Formulario para clientes creados"""

    def __init__(self, root, db, fecha_registro, callback_volver):
        self.root = root
        self.db = db
        self.fecha_registro = fecha_registro
        self.callback_volver = callback_volver

        self.crear_interfaz()

    def crear_interfaz(self):
        # Frame principal con scroll
        canvas = tk.Canvas(self.root, bg=COLOR_BLANCO)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg=COLOR_BLANCO)

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Encabezado
        header = tk.Frame(frame, bg=COLOR_AZUL, height=100)
        header.pack(fill='x', pady=(0, 20))
        tk.Label(header, text="Formulario Rayogas ESP",
                font=('Arial', 18, 'bold'), fg=COLOR_BLANCO, bg=COLOR_AZUL).pack(pady=5)
        tk.Label(header, text="Puntos Colombia - Clientes Creados",
                font=('Arial', 12), fg=COLOR_BLANCO, bg=COLOR_AZUL).pack(pady=5)

        # Formulario
        form_frame = tk.Frame(frame, bg=COLOR_GRIS_CLARO, relief='raised', borderwidth=2)
        form_frame.pack(fill='both', padx=30, pady=10)

        # Campos
        self.entries = {}
        campos = [
            ("Nombre Completo", "nombre_completo"),
            ("Cédula", "cedula"),
            ("Dirección", "direccion"),
            ("Zona", "zona"),
            ("Puntos Acumulados por la Compra", "puntos_acumulados")
        ]

        for i, (label, key) in enumerate(campos):
            tk.Label(form_frame, text=f"{label}:", font=('Arial', 11, 'bold'),
                    bg=COLOR_GRIS_CLARO).grid(row=i, column=0, sticky='w', padx=20, pady=10)
            entry = tk.Entry(form_frame, font=('Arial', 11), width=40)
            entry.grid(row=i, column=1, padx=20, pady=10)
            self.entries[key] = entry

        # Botones
        btn_frame = tk.Frame(frame, bg=COLOR_BLANCO)
        btn_frame.pack(pady=30)

        tk.Button(btn_frame, text="Volver", font=('Arial', 11, 'bold'),
                 bg='#6c757d', fg=COLOR_BLANCO, width=15, height=2,
                 cursor='hand2', command=self.volver).pack(side='left', padx=10)

        tk.Button(btn_frame, text="Guardar Registro", font=('Arial', 11, 'bold'),
                 bg=COLOR_AZUL, fg=COLOR_BLANCO, width=20, height=2,
                 cursor='hand2', command=self.guardar).pack(side='left', padx=10)

    def guardar(self):
        # Validar campos
        for key, entry in self.entries.items():
            if not entry.get().strip():
                messagebox.showwarning("Advertencia", "Por favor complete todos los campos")
                return

        try:
            datos = (
                self.fecha_registro,
                self.entries['nombre_completo'].get(),
                self.entries['cedula'].get(),
                self.entries['direccion'].get(),
                self.entries['zona'].get(),
                int(self.entries['puntos_acumulados'].get())
            )

            self.db.guardar_cliente_creado(datos)
            messagebox.showinfo("Éxito", "Registro guardado exitosamente")
            self.volver()

        except ValueError:
            messagebox.showerror("Error", "Los puntos acumulados deben ser un número")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    def volver(self):
        self.callback_volver()


class VentanaClienteNuevo:
    """Formulario para clientes nuevos"""

    def __init__(self, root, db, fecha_registro, callback_volver):
        self.root = root
        self.db = db
        self.fecha_registro = fecha_registro
        self.callback_volver = callback_volver
        self.archivo_cedula = None

        self.crear_interfaz()

    def crear_interfaz(self):
        # Frame principal con scroll
        canvas = tk.Canvas(self.root, bg=COLOR_BLANCO)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg=COLOR_BLANCO)

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Encabezado
        header = tk.Frame(frame, bg=COLOR_AZUL, height=100)
        header.pack(fill='x', pady=(0, 20))
        tk.Label(header, text="Formulario Rayogas ESP",
                font=('Arial', 18, 'bold'), fg=COLOR_BLANCO, bg=COLOR_AZUL).pack(pady=5)
        tk.Label(header, text="Puntos Colombia - Clientes Nuevos",
                font=('Arial', 12), fg=COLOR_BLANCO, bg=COLOR_AZUL).pack(pady=5)

        # Formulario
        form_frame = tk.Frame(frame, bg=COLOR_GRIS_CLARO, relief='raised', borderwidth=2)
        form_frame.pack(fill='both', padx=30, pady=10)

        row = 0
        self.entries = {}

        # Campos de texto
        campos_texto = [
            ("Nombre Completo", "nombre_completo"),
            ("Cédula", "cedula"),
            ("Celular o Número de Contacto", "celular"),
            ("Ciudad o Municipio", "ciudad"),
            ("Zona", "zona"),
            ("Dirección", "direccion")
        ]

        for label, key in campos_texto:
            tk.Label(form_frame, text=f"{label}:", font=('Arial', 10, 'bold'),
                    bg=COLOR_GRIS_CLARO).grid(row=row, column=0, sticky='w', padx=15, pady=8)
            entry = tk.Entry(form_frame, font=('Arial', 10), width=40)
            entry.grid(row=row, column=1, padx=15, pady=8)
            self.entries[key] = entry
            row += 1

        # Uso del gas
        tk.Label(form_frame, text="Uso del Gas GLP:", font=('Arial', 10, 'bold'),
                bg=COLOR_GRIS_CLARO).grid(row=row, column=0, sticky='w', padx=15, pady=8)
        self.combo_uso_gas = ttk.Combobox(form_frame, font=('Arial', 10), width=38,
                                         values=["Residencial", "Industrial", "Comercial"],
                                         state='readonly')
        self.combo_uso_gas.grid(row=row, column=1, padx=15, pady=8)
        row += 1

        # Inscrito en puntos
        tk.Label(form_frame, text="¿Inscrito en Puntos Colombia?:", font=('Arial', 10, 'bold'),
                bg=COLOR_GRIS_CLARO).grid(row=row, column=0, sticky='w', padx=15, pady=8)
        self.var_inscrito = tk.StringVar()
        radio_frame1 = tk.Frame(form_frame, bg=COLOR_GRIS_CLARO)
        radio_frame1.grid(row=row, column=1, sticky='w', padx=15, pady=8)
        tk.Radiobutton(radio_frame1, text="SI", variable=self.var_inscrito, value="SI",
                      bg=COLOR_GRIS_CLARO).pack(side='left', padx=10)
        tk.Radiobutton(radio_frame1, text="NO", variable=self.var_inscrito, value="NO",
                      bg=COLOR_GRIS_CLARO).pack(side='left', padx=10)
        row += 1

        # Monto de compra
        tk.Label(form_frame, text="Monto de la Compra:", font=('Arial', 10, 'bold'),
                bg=COLOR_GRIS_CLARO).grid(row=row, column=0, sticky='w', padx=15, pady=8)
        self.entry_monto = tk.Entry(form_frame, font=('Arial', 10), width=40)
        self.entry_monto.grid(row=row, column=1, padx=15, pady=8)
        row += 1

        # Puntos acumulados
        tk.Label(form_frame, text="Puntos Acumulados:", font=('Arial', 10, 'bold'),
                bg=COLOR_GRIS_CLARO).grid(row=row, column=0, sticky='w', padx=15, pady=8)
        self.entry_puntos = tk.Entry(form_frame, font=('Arial', 10), width=40)
        self.entry_puntos.grid(row=row, column=1, padx=15, pady=8)
        row += 1

        # Autorización
        autorizacion_frame = tk.Frame(form_frame, bg=COLOR_BLANCO, relief='groove', borderwidth=2)
        autorizacion_frame.grid(row=row, column=0, columnspan=2, padx=15, pady=15, sticky='ew')

        tk.Label(autorizacion_frame, text="Autorización para tratamiento de datos personales",
                font=('Arial', 10, 'bold'), bg=COLOR_BLANCO).pack(pady=5)

        texto_autorizacion = ("Autorizo de manera libre, expresa y voluntaria a RAYOGAS S.A.S. para recolectar, "
                             "almacenar y usar mis datos personales con el fin de contactarme, brindarme información "
                             "sobre beneficios, promociones, programas de fidelización (incluyendo Puntos Colombia) "
                             "y realizar actividades de servicio al cliente. Entiendo que podré ejercer mis derechos "
                             "de conocer, actualizar y suprimir mi información en cualquier momento, conforme a la "
                             "Ley 1581 de 2012.")

        tk.Label(autorizacion_frame, text=texto_autorizacion, wraplength=550, justify='left',
                font=('Arial', 9), bg=COLOR_BLANCO).pack(pady=10, padx=10)

        self.var_autorizacion = tk.StringVar()
        radio_frame2 = tk.Frame(autorizacion_frame, bg=COLOR_BLANCO)
        radio_frame2.pack(pady=5)
        tk.Radiobutton(radio_frame2, text="ACEPTO", variable=self.var_autorizacion,
                      value="ACEPTO", bg=COLOR_BLANCO, font=('Arial', 10, 'bold')).pack(side='left', padx=20)
        tk.Radiobutton(radio_frame2, text="NO ACEPTO", variable=self.var_autorizacion,
                      value="NO ACEPTO", bg=COLOR_BLANCO, font=('Arial', 10, 'bold')).pack(side='left', padx=20)
        row += 1

        # Archivo adjunto
        tk.Label(form_frame, text="Adjunte foto de Cédula\n(Ambas caras):", font=('Arial', 10, 'bold'),
                bg=COLOR_GRIS_CLARO).grid(row=row, column=0, sticky='w', padx=15, pady=8)

        archivo_frame = tk.Frame(form_frame, bg=COLOR_GRIS_CLARO)
        archivo_frame.grid(row=row, column=1, padx=15, pady=8, sticky='w')

        self.label_archivo = tk.Label(archivo_frame, text="Ningún archivo seleccionado",
                                      font=('Arial', 9), bg=COLOR_BLANCO, width=30, anchor='w')
        self.label_archivo.pack(side='left', padx=5)

        tk.Button(archivo_frame, text="Examinar...", command=self.seleccionar_archivo,
                 bg=COLOR_AZUL, fg=COLOR_BLANCO, cursor='hand2').pack(side='left')

        # Botones
        btn_frame = tk.Frame(frame, bg=COLOR_BLANCO)
        btn_frame.pack(pady=30)

        tk.Button(btn_frame, text="Volver", font=('Arial', 11, 'bold'),
                 bg='#6c757d', fg=COLOR_BLANCO, width=15, height=2,
                 cursor='hand2', command=self.volver).pack(side='left', padx=10)

        tk.Button(btn_frame, text="Guardar Registro", font=('Arial', 11, 'bold'),
                 bg=COLOR_AZUL, fg=COLOR_BLANCO, width=20, height=2,
                 cursor='hand2', command=self.guardar).pack(side='left', padx=10)

    def seleccionar_archivo(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de cédula",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png"), ("PDF", "*.pdf"), ("Todos", "*.*")]
        )
        if filename:
            self.archivo_cedula = filename
            self.label_archivo.config(text=os.path.basename(filename))

    def guardar(self):
        # Validar campos
        for key, entry in self.entries.items():
            if not entry.get().strip():
                messagebox.showwarning("Advertencia", "Por favor complete todos los campos")
                return

        if not self.combo_uso_gas.get():
            messagebox.showwarning("Advertencia", "Por favor seleccione el uso del gas")
            return

        if not self.var_inscrito.get():
            messagebox.showwarning("Advertencia", "Por favor indique si está inscrito en Puntos Colombia")
            return

        if not self.entry_monto.get().strip() or not self.entry_puntos.get().strip():
            messagebox.showwarning("Advertencia", "Por favor complete el monto y los puntos")
            return

        if not self.var_autorizacion.get():
            messagebox.showwarning("Advertencia", "Por favor indique su autorización para tratamiento de datos")
            return

        if not self.archivo_cedula:
            messagebox.showwarning("Advertencia", "Por favor adjunte la foto de su cédula")
            return

        try:
            # Copiar archivo
            if not os.path.exists('uploads'):
                os.makedirs('uploads')

            cedula = self.entries['cedula'].get()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            ext = os.path.splitext(self.archivo_cedula)[1]
            nombre_archivo = f"{cedula}_{timestamp}{ext}"
            destino = os.path.join('uploads', nombre_archivo)
            shutil.copy2(self.archivo_cedula, destino)

            datos = (
                self.fecha_registro,
                self.entries['nombre_completo'].get(),
                self.entries['cedula'].get(),
                self.entries['celular'].get(),
                self.entries['ciudad'].get(),
                self.entries['zona'].get(),
                self.entries['direccion'].get(),
                self.combo_uso_gas.get(),
                self.var_inscrito.get(),
                float(self.entry_monto.get()),
                int(self.entry_puntos.get()),
                self.var_autorizacion.get(),
                nombre_archivo
            )

            self.db.guardar_cliente_nuevo(datos)
            messagebox.showinfo("Éxito", "Registro guardado exitosamente")
            self.volver()

        except ValueError:
            messagebox.showerror("Error", "El monto y los puntos deben ser números válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    def volver(self):
        self.callback_volver()


class AplicacionRayogas:
    """Aplicación principal"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Formulario Rayogas ESP - Puntos Colombia")
        self.root.geometry("800x600")
        self.root.configure(bg=COLOR_BLANCO)

        # Centrar ventana
        self.centrar_ventana(800, 600)

        # Base de datos
        self.db = BaseDatos()

        # Mostrar login
        self.mostrar_login()

    def centrar_ventana(self, ancho, alto):
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        self.limpiar_ventana()
        self.root.geometry("500x500")
        self.centrar_ventana(500, 500)
        VentanaLogin(self.root, self.mostrar_formulario_principal)

    def mostrar_formulario_principal(self):
        self.limpiar_ventana()
        self.root.geometry("700x500")
        self.centrar_ventana(700, 500)
        VentanaFormularioPrincipal(self.root, self.db,
                                  self.mostrar_formulario_cliente_creado,
                                  self.mostrar_formulario_cliente_nuevo)

    def mostrar_formulario_cliente_creado(self, fecha_registro):
        self.limpiar_ventana()
        self.root.geometry("700x600")
        self.centrar_ventana(700, 600)
        VentanaClienteCreado(self.root, self.db, fecha_registro,
                           self.mostrar_formulario_principal)

    def mostrar_formulario_cliente_nuevo(self, fecha_registro):
        self.limpiar_ventana()
        self.root.geometry("700x800")
        self.centrar_ventana(700, 800)
        VentanaClienteNuevo(self.root, self.db, fecha_registro,
                          self.mostrar_formulario_principal)

    def ejecutar(self):
        self.root.mainloop()
        self.db.cerrar()


if __name__ == "__main__":
    app = AplicacionRayogas()
    app.ejecutar()
