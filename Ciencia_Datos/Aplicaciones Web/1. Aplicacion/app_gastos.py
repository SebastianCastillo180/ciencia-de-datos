import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import hashlib

class SistemaGastos:
    def __init__(self):
        self.archivo_usuarios = 'usuarios.json'
        self.archivo_gastos = 'gastos.json'
        self.usuario_actual = None
        self.cargar_datos()
        
    def cargar_datos(self):

#########################################################################
        """Carga usuarios y gastos desde archivos JSON"""
        # Cargar usuarios
        if os.path.exists(self.archivo_usuarios):
            with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                self.usuarios = json.load(f)
        else:
#########################################################################
            # Usuario por defecto: admin / admin123
            self.usuarios = {
                'admin': {
                    'password': self.hash_password('admin123'),
                    'nombre': 'Administrador',
                    'rol': 'admin'
                }
            }
            self.guardar_usuarios()
        
        # Cargar gastos
        if os.path.exists(self.archivo_gastos):
            with open(self.archivo_gastos, 'r', encoding='utf-8') as f:
                self.gastos = json.load(f)
        else:
            self.gastos = []
            self.guardar_gastos()
    
    def hash_password(self, password):
        """Encripta la contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def guardar_usuarios(self):
        """Guarda usuarios en archivo JSON"""
        with open(self.archivo_usuarios, 'w', encoding='utf-8') as f:
            json.dump(self.usuarios, f, indent=4, ensure_ascii=False)
    
    def guardar_gastos(self):
        """Guarda gastos en archivo JSON"""
        with open(self.archivo_gastos, 'w', encoding='utf-8') as f:
            json.dump(self.gastos, f, indent=4, ensure_ascii=False)
    
    def verificar_login(self, usuario, password):
        """Verifica credenciales de login"""
        if usuario in self.usuarios:
            if self.usuarios[usuario]['password'] == self.hash_password(password):
                self.usuario_actual = usuario
                return True
        return False
    
    def registrar_usuario(self, usuario, password, nombre):
        """Registra un nuevo usuario"""
        if usuario in self.usuarios:
            return False
        self.usuarios[usuario] = {
            'password': self.hash_password(password),
            'nombre': nombre,
            'rol': 'usuario'
        }
        self.guardar_usuarios()
        return True
    
    def agregar_gasto(self, descripcion, monto, categoria, fecha):
#########################################################################
        """Agrega un nuevo gasto"""
        gasto = {
            'id': len(self.gastos) + 1,
            'usuario': self.usuario_actual,
            'nombre_usuario': self.usuarios[self.usuario_actual]['nombre'],
            'descripcion': descripcion,
            'monto': float(monto),
            'categoria': categoria,
            'fecha': fecha,
            'estado': 'Pendiente',
            'fecha_registro': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.gastos.append(gasto)
        self.guardar_gastos()
        return True
    
    def obtener_gastos_usuario(self):
        """Obtiene gastos del usuario actual"""
        return [g for g in self.gastos if g['usuario'] == self.usuario_actual]
    
    def obtener_todos_gastos(self):
        """Obtiene todos los gastos (solo admin)"""
        if self.usuarios[self.usuario_actual]['rol'] == 'admin':
            return self.gastos
        return self.obtener_gastos_usuario()
    
    def aprobar_gasto(self, gasto_id, estado):
        """Aprueba o rechaza un gasto"""
        for gasto in self.gastos:
            if gasto['id'] == gasto_id:
                gasto['estado'] = estado
                self.guardar_gastos()
                return True
        return False


class VentanaLogin:
    def __init__(self, sistema):
        self.sistema = sistema
        self.ventana = tk.Tk()
        self.ventana.title("Login - Sistema de Legalización de Gastos")
        self.ventana.geometry("400x350")
        self.ventana.configure(bg='#2c3e50')
        
        # Centrar ventana
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
        # Marco principal
        marco = tk.Frame(self.ventana, bg='#ecf0f1', padx=30, pady=30)
        marco.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        titulo = tk.Label(marco, text="🔐 SISTEMA DE GASTOS", 
                         font=('Arial', 18, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        titulo.pack(pady=(0, 20))
        
        # Usuario
        tk.Label(marco, text="Usuario:", font=('Arial', 11), 
                bg='#ecf0f1', fg='#2c3e50').pack(anchor='w', pady=(10, 5))
        self.entry_usuario = tk.Entry(marco, font=('Arial', 11), width=30)
        self.entry_usuario.pack(pady=(0, 10))
        
        # Contraseña
        tk.Label(marco, text="Contraseña:", font=('Arial', 11), 
                bg='#ecf0f1', fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        self.entry_password = tk.Entry(marco, font=('Arial', 11), 
                                       width=30, show='*')
        self.entry_password.pack(pady=(0, 20))
        
        # Botones
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
        
        # Info por defecto
        info = tk.Label(marco, text="Usuario por defecto: admin / admin123", 
                       font=('Arial', 9, 'italic'), bg='#ecf0f1', fg='#7f8c8d')
        info.pack(pady=(15, 0))
        
        # Enter para login
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
        
        # Nombre completo
        tk.Label(marco, text="Nombre completo:", font=('Arial', 11), 
                bg='#ecf0f1', fg='#2c3e50').pack(anchor='w', pady=(5, 5))
        self.entry_nombre = tk.Entry(marco, font=('Arial', 11), width=30)
        self.entry_nombre.pack(pady=(0, 10))
        
        # Usuario
        tk.Label(marco, text="Usuario:", font=('Arial', 11), 
                bg='#ecf0f1', fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        self.entry_usuario = tk.Entry(marco, font=('Arial', 11), width=30)
        self.entry_usuario.pack(pady=(0, 10))
        
        # Contraseña
        tk.Label(marco, text="Contraseña:", font=('Arial', 11), 
                bg='#ecf0f1', fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        self.entry_password = tk.Entry(marco, font=('Arial', 11), 
                                       width=30, show='*')
        self.entry_password.pack(pady=(0, 20))
        
        # Botones
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
        self.ventana.title("Sistema de Legalización de Gastos")
        self.ventana.geometry("1000x600")
        self.ventana.configure(bg='#ecf0f1')
        
        self.crear_interfaz()
        self.cargar_gastos()
        
    def crear_interfaz(self):
        # Encabezado
        header = tk.Frame(self.ventana, bg='#2c3e50', height=60)
        header.pack(fill='x')
        
        usuario_info = f"👤 {self.sistema.usuarios[self.sistema.usuario_actual]['nombre']}"
        tk.Label(header, text=usuario_info, font=('Arial', 12, 'bold'), 
                bg='#2c3e50', fg='white').pack(side='left', padx=20, pady=15)
        
        btn_cerrar = tk.Button(header, text="Cerrar Sesión", 
                              command=self.cerrar_sesion,
                              font=('Arial', 10), bg='#e74c3c', fg='white',
                              cursor='hand2')
        btn_cerrar.pack(side='right', padx=20, pady=15)
        
        # Contenedor principal
        contenedor = tk.Frame(self.ventana, bg='#ecf0f1')
        contenedor.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Nuevo gasto
        panel_izq = tk.LabelFrame(contenedor, text="➕ Nuevo Gasto", 
                                 font=('Arial', 12, 'bold'),
                                 bg='white', padx=15, pady=15)
        panel_izq.pack(side='left', fill='both', padx=(0, 5), pady=5)
        
        # Formulario
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
                                          'Hospedaje', 'Material', 'Otros')
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
        
        # Tabla de gastos
        frame_tabla = tk.Frame(panel_der, bg='white')
        frame_tabla.pack(fill='both', expand=True)
        
        # Scrollbars
        scroll_y = tk.Scrollbar(frame_tabla)
        scroll_y.pack(side='right', fill='y')
        
        scroll_x = tk.Scrollbar(frame_tabla, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')
        
        # Treeview
        columnas = ('ID', 'Descripción', 'Monto', 'Categoría', 'Fecha', 'Estado')
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show='headings',
                                 yscrollcommand=scroll_y.set,
                                 xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)
        
        # Configurar columnas
        self.tabla.heading('ID', text='ID')
        self.tabla.heading('Descripción', text='Descripción')
        self.tabla.heading('Monto', text='Monto')
        self.tabla.heading('Categoría', text='Categoría')
        self.tabla.heading('Fecha', text='Fecha')
        self.tabla.heading('Estado', text='Estado')
        
        self.tabla.column('ID', width=50, anchor='center')
        self.tabla.column('Descripción', width=200)
        self.tabla.column('Monto', width=100, anchor='center')
        self.tabla.column('Categoría', width=100, anchor='center')
        self.tabla.column('Fecha', width=100, anchor='center')
        self.tabla.column('Estado', width=100, anchor='center')
        
        self.tabla.pack(fill='both', expand=True)
        
        # Botones de acción (solo para admin)
        if self.sistema.usuarios[self.sistema.usuario_actual]['rol'] == 'admin':
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
    
    def cargar_gastos(self):
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Cargar gastos
        gastos = self.sistema.obtener_todos_gastos()
        
        for gasto in gastos:
            self.tabla.insert('', 'end', values=(
                gasto['id'],
                gasto['descripcion'],
                f"${gasto['monto']:.2f}",
                gasto['categoria'],
                gasto['fecha'],
                gasto['estado']
            ))
    
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
    
    def cerrar_sesion(self):
        if messagebox.askyesno("Confirmar", "¿Desea cerrar sesión?"):
            self.ventana.destroy()
            VentanaLogin(self.sistema).iniciar()
    
    def iniciar(self):
        self.ventana.mainloop()


# Iniciar aplicación
if __name__ == "__main__":
    sistema = SistemaGastos()
    app = VentanaLogin(sistema)
    app.iniciar()
