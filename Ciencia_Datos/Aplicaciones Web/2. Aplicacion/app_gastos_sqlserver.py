#####################################################################################################
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import hashlib
import pyodbc

class ConexionSQL:
    def __init__(self):
#####################################################################################################
        """Configuración de conexión a SQL Server"""
        self.server = '192.168.0.22'
        self.database = 'Replica'
        self.username = 'siesarayo'  # Cambiar por tu usuario
        self.password = 'SisR@yos.2017'  # Cambiar por tu contraseña
        self.conn = None
        
    def conectar(self):
#####################################################################################################
        """Establece conexión con SQL Server"""
        try:
            connection_string = (
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={self.server};'
                f'DATABASE={self.database};'
                f'UID={self.username};'
                f'PWD={self.password}'
            )
            self.conn = pyodbc.connect(connection_string)
            return True
        except pyodbc.Error as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a SQL Server:\n{str(e)}")
            return False
    
    def desconectar(self):
#####################################################################################################
        """Cierra la conexión"""
        if self.conn:
            self.conn.close()
#####################################################################################################    
    def crear_tablas(self):
        """Crea las tablas necesarias si no existen"""
        try:
            cursor = self.conn.cursor()
            
            # Tabla de usuarios
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Usuarios' AND xtype='U')
                CREATE TABLE Usuarios (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    usuario VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    nombre VARCHAR(100) NOT NULL,
                    rol VARCHAR(20) DEFAULT 'usuario',
                    fecha_registro DATETIME DEFAULT GETDATE(),
                    activo BIT DEFAULT 1
                )
            """)
            
            # Tabla de gastos
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Gastos' AND xtype='U')
                CREATE TABLE Gastos (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    usuario_id INT NOT NULL,
                    descripcion VARCHAR(500) NOT NULL,
                    monto DECIMAL(10,2) NOT NULL,
                    categoria VARCHAR(50) NOT NULL,
                    fecha_gasto DATE NOT NULL,
                    estado VARCHAR(20) DEFAULT 'Pendiente',
                    fecha_registro DATETIME DEFAULT GETDATE(),
                    aprobado_por INT NULL,
                    fecha_aprobacion DATETIME NULL,
                    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id)
                )
            """)
            
            # Tabla de comentarios (opcional)
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Comentarios' AND xtype='U')
                CREATE TABLE Comentarios (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    gasto_id INT NOT NULL,
                    usuario_id INT NOT NULL,
                    comentario TEXT,
                    fecha DATETIME DEFAULT GETDATE(),
                    FOREIGN KEY (gasto_id) REFERENCES Gastos(id),
                    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id)
                )
            """)
            
            self.conn.commit()
#####################################################################################################           
            # Crear usuario admin por defecto si no existe
            cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE usuario = 'admin'")
            if cursor.fetchone()[0] == 0:
                password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
                cursor.execute("""
                    INSERT INTO Usuarios (usuario, password, nombre, rol) 
                    VALUES (?, ?, ?, ?)
                """, ('admin', password_hash, 'Administrador', 'admin'))
                self.conn.commit()
            
            return True
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"Error al crear tablas:\n{str(e)}")
            return False


class SistemaGastos:
    def __init__(self):
        self.db = ConexionSQL()
        self.usuario_actual = None
        self.usuario_id = None
#####################################################################################################        
        # Intentar conectar
        if not self.db.conectar():
            messagebox.showerror("Error Fatal", "No se pudo conectar a la base de datos.\nVerifique la configuración.")
            return
#####################################################################################################        
        # Crear tablas si no existen
        self.db.crear_tablas()
        
    def hash_password(self, password):
        """Encripta la contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verificar_login(self, usuario, password):
        """Verifica credenciales de login"""
        try:
            cursor = self.db.conn.cursor()
            password_hash = self.hash_password(password)
            
            cursor.execute("""
                SELECT id, nombre, rol FROM Usuarios 
                WHERE usuario = ? AND password = ? AND activo = 1
            """, (usuario, password_hash))
            
            resultado = cursor.fetchone()
            
            if resultado:
                self.usuario_id = resultado[0]
                self.usuario_actual = usuario
                self.usuario_nombre = resultado[1]
                self.usuario_rol = resultado[2]
                return True
            return False
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"Error al verificar login:\n{str(e)}")
            return False
    
    def registrar_usuario(self, usuario, password, nombre):
        """Registra un nuevo usuario"""
        try:
            cursor = self.db.conn.cursor()
            password_hash = self.hash_password(password)
#####################################################################################################            
            # Verificar si el usuario ya existe
            cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE usuario = ?", (usuario,))
            if cursor.fetchone()[0] > 0:
                return False
#####################################################################################################            
            # Insertar nuevo usuario
            cursor.execute("""
                INSERT INTO Usuarios (usuario, password, nombre, rol) 
                VALUES (?, ?, ?, ?)
            """, (usuario, password_hash, nombre, 'usuario'))
            
            self.db.conn.commit()
            return True
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"Error al registrar usuario:\n{str(e)}")
            return False
    
    def agregar_gasto(self, descripcion, monto, categoria, fecha):
        """Agrega un nuevo gasto"""
        try:
            cursor = self.db.conn.cursor()
            
            cursor.execute("""
                INSERT INTO Gastos (usuario_id, descripcion, monto, categoria, fecha_gasto, estado) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.usuario_id, descripcion, float(monto), categoria, fecha, 'Pendiente'))
            
            self.db.conn.commit()
            return True
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"Error al agregar gasto:\n{str(e)}")
            return False
    
    def obtener_gastos_usuario(self):
        """Obtiene gastos del usuario actual"""
        try:
            cursor = self.db.conn.cursor()
            
            cursor.execute("""
                SELECT g.id, g.descripcion, g.monto, g.categoria, 
                       g.fecha_gasto, g.estado, g.fecha_registro
                FROM Gastos g
                WHERE g.usuario_id = ?
                ORDER BY g.fecha_registro DESC
            """, (self.usuario_id,))
            
            return cursor.fetchall()
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"Error al obtener gastos:\n{str(e)}")
            return []
    
    def obtener_todos_gastos(self):
        """Obtiene todos los gastos (solo admin)"""
        try:
            cursor = self.db.conn.cursor()
            
            if self.usuario_rol == 'admin':
                cursor.execute("""
                    SELECT g.id, u.nombre, g.descripcion, g.monto, g.categoria, 
                           g.fecha_gasto, g.estado, g.fecha_registro
                    FROM Gastos g
                    INNER JOIN Usuarios u ON g.usuario_id = u.id
                    ORDER BY g.fecha_registro DESC
                """)
            else:
                cursor.execute("""
                    SELECT g.id, g.descripcion, g.monto, g.categoria, 
                           g.fecha_gasto, g.estado, g.fecha_registro
                    FROM Gastos g
                    WHERE g.usuario_id = ?
                    ORDER BY g.fecha_registro DESC
                """, (self.usuario_id,))
            
            return cursor.fetchall()
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"Error al obtener gastos:\n{str(e)}")
            return []
    
    def aprobar_gasto(self, gasto_id, estado):
        """Aprueba o rechaza un gasto"""
        try:
            cursor = self.db.conn.cursor()
            
            cursor.execute("""
                UPDATE Gastos 
                SET estado = ?, aprobado_por = ?, fecha_aprobacion = GETDATE()
                WHERE id = ?
            """, (estado, self.usuario_id, gasto_id))
            
            self.db.conn.commit()
            return True
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"Error al aprobar gasto:\n{str(e)}")
            return False
    
    def obtener_estadisticas(self):
        """Obtiene estadísticas de gastos"""
        try:
            cursor = self.db.conn.cursor()
            
            if self.usuario_rol == 'admin':
                # Estadísticas generales
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN estado = 'Pendiente' THEN 1 ELSE 0 END) as pendientes,
                        SUM(CASE WHEN estado = 'Aprobado' THEN 1 ELSE 0 END) as aprobados,
                        SUM(CASE WHEN estado = 'Rechazado' THEN 1 ELSE 0 END) as rechazados,
                        SUM(monto) as monto_total
                    FROM Gastos
                """)
            else:
                # Estadísticas del usuario
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN estado = 'Pendiente' THEN 1 ELSE 0 END) as pendientes,
                        SUM(CASE WHEN estado = 'Aprobado' THEN 1 ELSE 0 END) as aprobados,
                        SUM(CASE WHEN estado = 'Rechazado' THEN 1 ELSE 0 END) as rechazados,
                        SUM(monto) as monto_total
                    FROM Gastos
                    WHERE usuario_id = ?
                """, (self.usuario_id,))
            
            return cursor.fetchone()
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"Error al obtener estadísticas:\n{str(e)}")
            return (0, 0, 0, 0, 0)


class VentanaLogin:
    def __init__(self, sistema):
        self.sistema = sistema
        self.ventana = tk.Tk()
        self.ventana.title("Login - Sistema de Legalización de Gastos")
        self.ventana.geometry("400x350")
        self.ventana.configure(bg='#2c3e50')
        
        self.centrar_ventana()
        self.crear_interfaz()
        
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.ventana.update_idletasks()
        width = self.ventana.winfo_width()
        height = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (width // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (height // 2)
        self.ventana.geometry(f'{width}x{height}+{x}+{y}')
    
    def crear_interfaz(self):
        marco = tk.Frame(self.ventana, bg='#ecf0f1', padx=30, pady=30)
        marco.pack(expand=True, fill='both', padx=20, pady=20)
        
        titulo = tk.Label(marco, text="🔐 SISTEMA DE GASTOS", 
                         font=('Arial', 18, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        titulo.pack(pady=(0, 10))
        
        subtitulo = tk.Label(marco, text="SQL Server Edition", 
                            font=('Arial', 10, 'italic'), bg='#ecf0f1', fg='#7f8c8d')
        subtitulo.pack(pady=(0, 20))
        
        tk.Label(marco, text="Usuario:", font=('Arial', 11), 
                bg='#ecf0f1', fg='#2c3e50').pack(anchor='w', pady=(10, 5))
        self.entry_usuario = tk.Entry(marco, font=('Arial', 11), width=30)
        self.entry_usuario.pack(pady=(0, 10))
        
        tk.Label(marco, text="Contraseña:", font=('Arial', 11), 
                bg='#ecf0f1', fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        self.entry_password = tk.Entry(marco, font=('Arial', 11), 
                                       width=30, show='*')
        self.entry_password.pack(pady=(0, 20))
        
        btn_login = tk.Button(marco, text="Iniciar Sesión", 
                             command=self.iniciar_sesion,
                             font=('Arial', 11, 'bold'), 
                             bg='#3498db', fg='white',
                             cursor='hand2', width=20)
        btn_login.pack(pady=5)
        
        btn_registro = tk.Button(marco, text="Registrar Usuario", 
                                command=self.mostrar_registro,
                                font=('Arial', 10), 
                                bg='#95a5a6', fg='white',
                                cursor='hand2', width=20)
        btn_registro.pack(pady=5)
        
        info = tk.Label(marco, text="Usuario por defecto: admin / admin123", 
                       font=('Arial', 9, 'italic'), bg='#ecf0f1', fg='#7f8c8d')
        info.pack(pady=(15, 0))
        
        self.entry_password.bind('<Return>', lambda e: self.iniciar_sesion())
    
    def iniciar_sesion(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        
        if not usuario or not password:
            messagebox.showwarning("Advertencia", "Complete todos los campos")
            return
        
        if self.sistema.verificar_login(usuario, password):
            self.ventana.destroy()
            VentanaPrincipal(self.sistema)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    
    def mostrar_registro(self):
        VentanaRegistro(self.ventana, self.sistema)
    
    def iniciar(self):
        self.ventana.mainloop()


class VentanaRegistro:
    def __init__(self, parent, sistema):
        self.sistema = sistema
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registro de Usuario")
        self.ventana.geometry("400x350")
        self.ventana.configure(bg='#2c3e50')
        self.ventana.grab_set()
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        marco = tk.Frame(self.ventana, bg='#ecf0f1', padx=30, pady=30)
        marco.pack(expand=True, fill='both', padx=20, pady=20)
        
        titulo = tk.Label(marco, text="📝 NUEVO USUARIO", 
                         font=('Arial', 16, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        titulo.pack(pady=(0, 20))
        
        tk.Label(marco, text="Nombre completo:", font=('Arial', 11), 
                bg='#ecf0f1', fg='#2c3e50').pack(anchor='w', pady=(5, 5))
        self.entry_nombre = tk.Entry(marco, font=('Arial', 11), width=30)
        self.entry_nombre.pack(pady=(0, 10))
        
        tk.Label(marco, text="Usuario:", font=('Arial', 11), 
                bg='#ecf0f1', fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        self.entry_usuario = tk.Entry(marco, font=('Arial', 11), width=30)
        self.entry_usuario.pack(pady=(0, 10))
        
        tk.Label(marco, text="Contraseña:", font=('Arial', 11), 
                bg='#ecf0f1', fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        self.entry_password = tk.Entry(marco, font=('Arial', 11), 
                                       width=30, show='*')
        self.entry_password.pack(pady=(0, 20))
        
        frame_botones = tk.Frame(marco, bg='#ecf0f1')
        frame_botones.pack()
        
        btn_registrar = tk.Button(frame_botones, text="Registrar", 
                                 command=self.registrar,
                                 font=('Arial', 11, 'bold'), 
                                 bg='#27ae60', fg='white',
                                 cursor='hand2', width=12)
        btn_registrar.pack(side='left', padx=5)
        
        btn_cancelar = tk.Button(frame_botones, text="Cancelar", 
                                command=self.ventana.destroy,
                                font=('Arial', 11), 
                                bg='#e74c3c', fg='white',
                                cursor='hand2', width=12)
        btn_cancelar.pack(side='left', padx=5)
    
    def registrar(self):
        nombre = self.entry_nombre.get().strip()
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        
        if not nombre or not usuario or not password:
            messagebox.showwarning("Advertencia", "Complete todos los campos")
            return
        
        if len(password) < 6:
            messagebox.showwarning("Advertencia", 
                                  "La contraseña debe tener al menos 6 caracteres")
            return
        
        if self.sistema.registrar_usuario(usuario, password, nombre):
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", "El usuario ya existe")


class VentanaPrincipal:
    def __init__(self, sistema):
        self.sistema = sistema
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Legalización de Gastos - SQL Server")
        self.ventana.geometry("1100x650")
        self.ventana.configure(bg='#ecf0f1')
        
        self.crear_interfaz()
        self.cargar_gastos()
        self.actualizar_estadisticas()
        
    def crear_interfaz(self):
        # Encabezado
        header = tk.Frame(self.ventana, bg='#2c3e50', height=60)
        header.pack(fill='x')
        
        usuario_info = f"👤 {self.sistema.usuario_nombre} ({self.sistema.usuario_rol})"
        tk.Label(header, text=usuario_info, font=('Arial', 12, 'bold'), 
                bg='#2c3e50', fg='white').pack(side='left', padx=20, pady=15)
        
        tk.Label(header, text="🗄️ SQL Server: 192.168.0.22", 
                font=('Arial', 10), bg='#2c3e50', fg='#95a5a6').pack(side='left', padx=20)
        
        btn_actualizar = tk.Button(header, text="🔄 Actualizar", 
                                   command=self.cargar_gastos,
                                   font=('Arial', 10), bg='#3498db', fg='white',
                                   cursor='hand2')
        btn_actualizar.pack(side='right', padx=10, pady=15)
        
        btn_cerrar = tk.Button(header, text="Cerrar Sesión", 
                              command=self.cerrar_sesion,
                              font=('Arial', 10), bg='#e74c3c', fg='white',
                              cursor='hand2')
        btn_cerrar.pack(side='right', padx=10, pady=15)
        
        # Contenedor superior - Estadísticas
        frame_stats = tk.Frame(self.ventana, bg='#ecf0f1')
        frame_stats.pack(fill='x', padx=10, pady=(10, 0))
        
        self.lbl_stats = tk.Label(frame_stats, text="Cargando estadísticas...", 
                                 font=('Arial', 11), bg='white', 
                                 relief='solid', borderwidth=1, padx=20, pady=10)
        self.lbl_stats.pack(fill='x')
        
        # Contenedor principal
        contenedor = tk.Frame(self.ventana, bg='#ecf0f1')
        contenedor.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Nuevo gasto
        panel_izq = tk.LabelFrame(contenedor, text="➕ Nuevo Gasto", 
                                 font=('Arial', 12, 'bold'),
                                 bg='white', padx=15, pady=15)
        panel_izq.pack(side='left', fill='both', padx=(0, 5), pady=5)
        
        tk.Label(panel_izq, text="Descripción:", font=('Arial', 10), 
                bg='white').grid(row=0, column=0, sticky='w', pady=5)
        self.entry_descripcion = tk.Entry(panel_izq, font=('Arial', 10), width=25)
        self.entry_descripcion.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(panel_izq, text="Monto ($):", font=('Arial', 10), 
                bg='white').grid(row=1, column=0, sticky='w', pady=5)
        self.entry_monto = tk.Entry(panel_izq, font=('Arial', 10), width=25)
        self.entry_monto.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(panel_izq, text="Categoría:", font=('Arial', 10), 
                bg='white').grid(row=2, column=0, sticky='w', pady=5)
        self.combo_categoria = ttk.Combobox(panel_izq, font=('Arial', 10), 
                                           width=23, state='readonly')
        self.combo_categoria['values'] = ('Transporte', 'Alimentación', 
                                          'Hospedaje', 'Material', 'Servicios', 'Otros')
        self.combo_categoria.current(0)
        self.combo_categoria.grid(row=2, column=1, pady=5, padx=5)
        
        tk.Label(panel_izq, text="Fecha:", font=('Arial', 10), 
                bg='white').grid(row=3, column=0, sticky='w', pady=5)
        self.entry_fecha = tk.Entry(panel_izq, font=('Arial', 10), width=25)
        self.entry_fecha.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.entry_fecha.grid(row=3, column=1, pady=5, padx=5)
        
        btn_agregar = tk.Button(panel_izq, text="💾 Agregar Gasto", 
                               command=self.agregar_gasto,
                               font=('Arial', 11, 'bold'), 
                               bg='#3498db', fg='white',
                               cursor='hand2', width=25)
        btn_agregar.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Panel derecho - Lista de gastos
        panel_der = tk.LabelFrame(contenedor, text="📊 Gastos Registrados", 
                                 font=('Arial', 12, 'bold'),
                                 bg='white', padx=10, pady=10)
        panel_der.pack(side='right', fill='both', expand=True, padx=(5, 0), pady=5)
        
        frame_tabla = tk.Frame(panel_der, bg='white')
        frame_tabla.pack(fill='both', expand=True)
        
        scroll_y = tk.Scrollbar(frame_tabla)
        scroll_y.pack(side='right', fill='y')
        
        scroll_x = tk.Scrollbar(frame_tabla, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')
        
        if self.sistema.usuario_rol == 'admin':
            columnas = ('ID', 'Usuario', 'Descripción', 'Monto', 'Categoría', 'Fecha', 'Estado')
        else:
            columnas = ('ID', 'Descripción', 'Monto', 'Categoría', 'Fecha', 'Estado')
        
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show='headings',
                                 yscrollcommand=scroll_y.set,
                                 xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)
        
        for col in columnas:
            self.tabla.heading(col, text=col)
            if col == 'ID':
                self.tabla.column(col, width=50, anchor='center')
            elif col == 'Monto':
                self.tabla.column(col, width=100, anchor='center')
            elif col == 'Descripción':
                self.tabla.column(col, width=200)
            else:
                self.tabla.column(col, width=100, anchor='center')
        
        self.tabla.pack(fill='both', expand=True)
        
        if self.sistema.usuario_rol == 'admin':
            frame_botones = tk.Frame(panel_der, bg='white')
            frame_botones.pack(fill='x', pady=10)
            
            btn_aprobar = tk.Button(frame_botones, text="✓ Aprobar", 
                                   command=lambda: self.cambiar_estado('Aprobado'),
                                   font=('Arial', 10), 
                                   bg='#27ae60', fg='white',
                                   cursor='hand2')
            btn_aprobar.pack(side='left', padx=5)
            
            btn_rechazar = tk.Button(frame_botones, text="✗ Rechazar", 
                                    command=lambda: self.cambiar_estado('Rechazado'),
                                    font=('Arial', 10), 
                                    bg='#e74c3c', fg='white',
                                    cursor='hand2')
            btn_rechazar.pack(side='left', padx=5)
    
    def agregar_gasto(self):
        descripcion = self.entry_descripcion.get().strip()
        monto = self.entry_monto.get().strip()
        categoria = self.combo_categoria.get()
        fecha = self.entry_fecha.get().strip()
        
        if not descripcion or not monto:
            messagebox.showwarning("Advertencia", "Complete descripción y monto")
            return
        
        try:
            monto_float = float(monto)
            if monto_float <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido")
            return
        
        if self.sistema.agregar_gasto(descripcion, monto, categoria, fecha):
            messagebox.showinfo("Éxito", "Gasto agregado correctamente")
            self.entry_descripcion.delete(0, 'end')
            self.entry_monto.delete(0, 'end')
            self.entry_fecha.delete(0, 'end')
            self.entry_fecha.insert(0, datetime.now().strftime('%Y-%m-%d'))
            self.cargar_gastos()
            self.actualizar_estadisticas()
    
    def cargar_gastos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        gastos = self.sistema.obtener_todos_gastos()
        
        for gasto in gastos:
            if self.sistema.usuario_rol == 'admin':
                self.tabla.insert('', 'end', values=(
                    gasto[0],  # ID
                    gasto[1],  # Usuario
                    gasto[2],  # Descripción
                    f"${gasto[3]:.2f}",  # Monto
                    gasto[4],  # Categoría
                    gasto[5],  # Fecha
                    gasto[6]   # Estado
                ))
            else:
                self.tabla.insert('', 'end', values=(
                    gasto[0],  # ID
                    gasto[1],  # Descripción
                    f"${gasto[2]:.2f}",  # Monto
                    gasto[3],  # Categoría
                    gasto[4],  # Fecha
                    gasto[5]   # Estado
                ))
    
    def actualizar_estadisticas(self):
        stats = self.sistema.obtener_estadisticas()
        texto = (f"📊 Total: {stats[0]} | "
                f"⏳ Pendientes: {stats[1]} | "
                f"✅ Aprobados: {stats[2]} | "
                f"❌ Rechazados: {stats[3]} | "
                f"💰 Monto Total: ${stats[4] or 0:.2f}")
        self.lbl_stats.config(text=texto)
    
    def cambiar_estado(self, estado):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un gasto")
            return
        
        item = self.tabla.item(seleccion[0])
        gasto_id = int(item['values'][0])
        
        if self.sistema.aprobar_gasto(gasto_id, estado):
            messagebox.showinfo("Éxito", f"Gasto {estado.lower()}")
            self.cargar_gastos()
            self.actualizar_estadisticas()
    
    def cerrar_sesion(self):
        if messagebox.askyesno("Confirmar", "¿Desea cerrar sesión?"):
            self.ventana.destroy()
            self.sistema.db.desconectar()
            VentanaLogin(self.sistema).iniciar()
    
    def iniciar(self):
        self.ventana.mainloop()


# Iniciar aplicación
if __name__ == "__main__":
    sistema = SistemaGastos()
    if sistema.db.conn:  # Solo iniciar si la conexión fue exitosa
        app = VentanaLogin(sistema)
        app.iniciar()
