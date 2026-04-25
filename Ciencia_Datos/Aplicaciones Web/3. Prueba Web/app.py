"""
Sistema Web de Legalización de Gastos para Conductores
Aplicación Flask con autenticación y base de datos SQL Server
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import pyodbc
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_super_segura_cambiar_en_produccion'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# Configuración de SQL Server
SQL_CONFIG = {
    'server': '192.168.0.22',
    'database': 'Replica',
    'username': 'siesarayo',
    'password': 'SisR@yos.2017',
    'driver': 'ODBC Driver 17 for SQL Server'
}

# ============================================
# FUNCIONES DE BASE DE DATOS
# ============================================

def get_db_connection():
    """Crea y retorna una conexión a la base de datos"""
    try:
        connection_string = (
            f"DRIVER={{{SQL_CONFIG['driver']}}};"
            f"SERVER={SQL_CONFIG['server']};"
            f"DATABASE={SQL_CONFIG['database']};"
            f"UID={SQL_CONFIG['username']};"
            f"PWD={SQL_CONFIG['password']}"
        )
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        print(f"Error de conexión: {e}")
        return None

def init_database():
    """Inicializa la base de datos con las tablas necesarias"""
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Tabla de Conductores (Usuarios)
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Conductores' AND xtype='U')
            CREATE TABLE Conductores (
                id INT IDENTITY(1,1) PRIMARY KEY,
                codigo_conductor VARCHAR(20) UNIQUE NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE,
                telefono VARCHAR(20),
                password_hash VARCHAR(255) NOT NULL,
                rol VARCHAR(20) DEFAULT 'conductor' CHECK (rol IN ('conductor', 'supervisor', 'admin')),
                empresa VARCHAR(100),
                placa_vehiculo VARCHAR(20),
                tipo_vehiculo VARCHAR(50),
                fecha_registro DATETIME DEFAULT GETDATE(),
                activo BIT DEFAULT 1,
                ultimo_acceso DATETIME
            )
        """)
        
        # Tabla de Gastos
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Gastos' AND xtype='U')
            CREATE TABLE Gastos (
                id INT IDENTITY(1,1) PRIMARY KEY,
                conductor_id INT NOT NULL,
                fecha_gasto DATE NOT NULL,
                tipo_gasto VARCHAR(50) NOT NULL,
                descripcion VARCHAR(500) NOT NULL,
                monto DECIMAL(10,2) NOT NULL CHECK (monto > 0),
                kilometraje INT,
                ruta VARCHAR(200),
                comprobante_numero VARCHAR(50),
                estado VARCHAR(20) DEFAULT 'Pendiente' CHECK (estado IN ('Pendiente', 'Aprobado', 'Rechazado')),
                fecha_registro DATETIME DEFAULT GETDATE(),
                aprobado_por INT,
                fecha_aprobacion DATETIME,
                observaciones TEXT,
                FOREIGN KEY (conductor_id) REFERENCES Conductores(id),
                FOREIGN KEY (aprobado_por) REFERENCES Conductores(id)
            )
        """)
        
        # Tabla de Rutas
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Rutas' AND xtype='U')
            CREATE TABLE Rutas (
                id INT IDENTITY(1,1) PRIMARY KEY,
                conductor_id INT NOT NULL,
                fecha DATE NOT NULL,
                hora_inicio TIME,
                hora_fin TIME,
                origen VARCHAR(200) NOT NULL,
                destino VARCHAR(200) NOT NULL,
                kilometros DECIMAL(10,2),
                pasajeros INT,
                observaciones TEXT,
                fecha_registro DATETIME DEFAULT GETDATE(),
                FOREIGN KEY (conductor_id) REFERENCES Conductores(id)
            )
        """)
        
        # Tabla de Vehículos
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Vehiculos' AND xtype='U')
            CREATE TABLE app.Vehiculos (
                id INT IDENTITY(1,1) PRIMARY KEY,
                placa VARCHAR(20) UNIQUE NOT NULL,
                marca VARCHAR(50),
                modelo VARCHAR(50),
                año INT,
                tipo VARCHAR(50),
                conductor_asignado INT,
                empresa VARCHAR(100),
                estado VARCHAR(20) DEFAULT 'Activo',
                fecha_registro DATETIME DEFAULT GETDATE(),
                FOREIGN KEY (conductor_asignado) REFERENCES Conductores(id)
            )
        """)
        
        # Crear índices
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name='idx_conductor_id')
            CREATE INDEX idx_conductor_id ON Gastos(conductor_id)
        """)
        
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name='idx_fecha_gasto')
            CREATE INDEX idx_fecha_gasto ON Gastos(fecha_gasto)
        """)
        
        # Crear usuario admin por defecto si no existe
        cursor.execute("SELECT COUNT(*) FROM Conductores WHERE codigo_conductor = 'ADMIN'")
        if cursor.fetchone()[0] == 0:
            # Contraseña: admin123
            password_hash = generate_password_hash('admin123')
            cursor.execute("""
                INSERT INTO Conductores (codigo_conductor, nombre, apellido, password_hash, rol, empresa)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ('ADMIN', 'Administrador', 'Sistema', password_hash, 'admin', 'Sistema'))
        
        conn.commit()
        print("✅ Base de datos inicializada correctamente")
        return True
        
    except pyodbc.Error as e:
        print(f"❌ Error al inicializar base de datos: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# ============================================
# DECORADORES DE AUTENTICACIÓN
# ============================================

def login_required(f):
    """Decorador para rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicia sesión para acceder', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorador para rutas que requieren rol de admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicia sesión', 'warning')
            return redirect(url_for('login'))
        if session.get('rol') not in ['admin', 'supervisor']:
            flash('No tienes permisos para acceder a esta sección', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ============================================
# RUTAS DE AUTENTICACIÓN
# ============================================

@app.route('/')
def index():
    """Página principal - redirige según estado de sesión"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if request.method == 'POST':
        codigo = request.form.get('codigo_conductor', '').strip()
        password = request.form.get('password', '')
        
        if not codigo or not password:
            flash('Por favor completa todos los campos', 'warning')
            return render_template('login.html')
        
        conn = get_db_connection()
        if not conn:
            flash('Error de conexión a la base de datos', 'danger')
            return render_template('login.html')
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, codigo_conductor, nombre, apellido, password_hash, rol, empresa, activo
            FROM Conductores
            WHERE codigo_conductor = ?
        """, (codigo,))
        
        user = cursor.fetchone()
        
        if user and user[7]:  # Verificar que esté activo
            if check_password_hash(user[4], password):
                # Actualizar último acceso
                cursor.execute("""
                    UPDATE Conductores 
                    SET ultimo_acceso = GETDATE() 
                    WHERE id = ?
                """, (user[0],))
                conn.commit()
                
                # Crear sesión
                session.permanent = True
                session['user_id'] = user[0]
                session['codigo'] = user[1]
                session['nombre'] = user[2]
                session['apellido'] = user[3]
                session['rol'] = user[5]
                session['empresa'] = user[6]
                
                flash(f'¡Bienvenido {user[2]} {user[3]}!', 'success')
                cursor.close()
                conn.close()
                return redirect(url_for('dashboard'))
            else:
                flash('Contraseña incorrecta', 'danger')
        else:
            flash('Usuario no encontrado o inactivo', 'danger')
        
        cursor.close()
        conn.close()
    
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de nuevos conductores"""
    if request.method == 'POST':
        # Obtener datos del formulario
        codigo = request.form.get('codigo_conductor', '').strip().upper()
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        email = request.form.get('email', '').strip()
        telefono = request.form.get('telefono', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        empresa = request.form.get('empresa', '').strip()
        placa = request.form.get('placa_vehiculo', '').strip().upper()
        tipo_vehiculo = request.form.get('tipo_vehiculo', '').strip()
        
        # Validaciones
        if not all([codigo, nombre, apellido, password, password_confirm]):
            flash('Por favor completa los campos obligatorios', 'warning')
            return render_template('registro.html')
        
        if password != password_confirm:
            flash('Las contraseñas no coinciden', 'warning')
            return render_template('registro.html')
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'warning')
            return render_template('registro.html')
        
        conn = get_db_connection()
        if not conn:
            flash('Error de conexión a la base de datos', 'danger')
            return render_template('registro.html')
        
        cursor = conn.cursor()
        
        # Verificar si el código ya existe
        cursor.execute("SELECT COUNT(*) FROM Conductores WHERE codigo_conductor = ?", (codigo,))
        if cursor.fetchone()[0] > 0:
            flash('El código de conductor ya está registrado', 'warning')
            cursor.close()
            conn.close()
            return render_template('registro.html')
        
        # Registrar conductor
        try:
            password_hash = generate_password_hash(password)
            cursor.execute("""
                INSERT INTO Conductores 
                (codigo_conductor, nombre, apellido, email, telefono, password_hash, empresa, placa_vehiculo, tipo_vehiculo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (codigo, nombre, apellido, email, telefono, password_hash, empresa, placa, tipo_vehiculo))
            
            conn.commit()
            flash('Registro exitoso. Ya puedes iniciar sesión', 'success')
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
            
        except pyodbc.Error as e:
            flash(f'Error al registrar: {str(e)}', 'danger')
            conn.rollback()
        
        cursor.close()
        conn.close()
    
    return render_template('registro.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

# ============================================
# RUTAS PRINCIPALES
# ============================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal del conductor"""
    conn = get_db_connection()
    if not conn:
        flash('Error de conexión', 'danger')
        return redirect(url_for('logout'))
    
    cursor = conn.cursor()
    user_id = session['user_id']
    
    # Estadísticas del conductor
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN estado = 'Pendiente' THEN 1 ELSE 0 END) as pendientes,
            SUM(CASE WHEN estado = 'Aprobado' THEN 1 ELSE 0 END) as aprobados,
            SUM(CASE WHEN estado = 'Rechazado' THEN 1 ELSE 0 END) as rechazados,
            ISNULL(SUM(monto), 0) as total_monto,
            ISNULL(SUM(CASE WHEN estado = 'Aprobado' THEN monto ELSE 0 END), 0) as monto_aprobado
        FROM Gastos
        WHERE conductor_id = ?
    """, (user_id,))
    
    stats = cursor.fetchone()
    
    # Gastos recientes
    cursor.execute("""
        SELECT TOP 10 id, fecha_gasto, tipo_gasto, descripcion, monto, estado, fecha_registro
        FROM Gastos
        WHERE conductor_id = ?
        ORDER BY fecha_registro DESC
    """, (user_id,))
    
    gastos_recientes = cursor.fetchall()
    
    # Si es admin, obtener estadísticas generales
    stats_generales = None
    if session.get('rol') in ['admin', 'supervisor']:
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT conductor_id) as total_conductores,
                COUNT(*) as total_gastos,
                SUM(CASE WHEN estado = 'Pendiente' THEN 1 ELSE 0 END) as pendientes,
                ISNULL(SUM(monto), 0) as total_monto
            FROM Gastos
        """)
        stats_generales = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', 
                          stats=stats, 
                          gastos_recientes=gastos_recientes,
                          stats_generales=stats_generales)

@app.route('/gastos')
@login_required
def gastos():
    """Lista de gastos del conductor"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Filtros
    fecha_desde = request.args.get('fecha_desde', '')
    fecha_hasta = request.args.get('fecha_hasta', '')
    estado = request.args.get('estado', '')
    tipo = request.args.get('tipo', '')
    
    query = """
        SELECT id, fecha_gasto, tipo_gasto, descripcion, monto, 
               ruta, comprobante_numero, estado, fecha_registro
        FROM Gastos
        WHERE conductor_id = ?
    """
    params = [session['user_id']]
    
    if fecha_desde:
        query += " AND fecha_gasto >= ?"
        params.append(fecha_desde)
    if fecha_hasta:
        query += " AND fecha_gasto <= ?"
        params.append(fecha_hasta)
    if estado:
        query += " AND estado = ?"
        params.append(estado)
    if tipo:
        query += " AND tipo_gasto = ?"
        params.append(tipo)
    
    query += " ORDER BY fecha_gasto DESC, fecha_registro DESC"
    
    cursor.execute(query, params)
    gastos_list = cursor.fetchall()
    
    # Tipos de gastos para el filtro
    cursor.execute("""
        SELECT DISTINCT tipo_gasto 
        FROM Gastos 
        WHERE conductor_id = ?
        ORDER BY tipo_gasto
    """, (session['user_id'],))
    tipos_gasto = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return render_template('gastos.html', 
                          gastos=gastos_list,
                          tipos_gasto=tipos_gasto,
                          filtros={
                              'fecha_desde': fecha_desde,
                              'fecha_hasta': fecha_hasta,
                              'estado': estado,
                              'tipo': tipo
                          })

@app.route('/nuevo-gasto', methods=['GET', 'POST'])
@login_required
def nuevo_gasto():
    """Registrar nuevo gasto"""
    if request.method == 'POST':
        fecha_gasto = request.form.get('fecha_gasto')
        tipo_gasto = request.form.get('tipo_gasto')
        descripcion = request.form.get('descripcion', '').strip()
        monto = request.form.get('monto', '0')
        kilometraje = request.form.get('kilometraje', '')
        ruta = request.form.get('ruta', '').strip()
        comprobante = request.form.get('comprobante_numero', '').strip()
        
        # Validaciones
        if not all([fecha_gasto, tipo_gasto, descripcion, monto]):
            flash('Por favor completa los campos obligatorios', 'warning')
            return render_template('nuevo_gasto.html')
        
        try:
            monto_float = float(monto)
            if monto_float <= 0:
                raise ValueError
        except ValueError:
            flash('El monto debe ser un número mayor a 0', 'warning')
            return render_template('nuevo_gasto.html')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO Gastos 
                (conductor_id, fecha_gasto, tipo_gasto, descripcion, monto, 
                 kilometraje, ruta, comprobante_numero, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (session['user_id'], fecha_gasto, tipo_gasto, descripcion, 
                  monto_float, kilometraje or None, ruta, comprobante, 'Pendiente'))
            
            conn.commit()
            flash('Gasto registrado exitosamente', 'success')
            cursor.close()
            conn.close()
            return redirect(url_for('gastos'))
            
        except pyodbc.Error as e:
            flash(f'Error al registrar gasto: {str(e)}', 'danger')
            conn.rollback()
        
        cursor.close()
        conn.close()
    
    return render_template('nuevo_gasto.html')

@app.route('/editar-gasto/<int:gasto_id>', methods=['GET', 'POST'])
@login_required
def editar_gasto(gasto_id):
    """Editar un gasto existente (solo si está pendiente)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verificar que el gasto pertenece al usuario y está pendiente
    cursor.execute("""
        SELECT id, fecha_gasto, tipo_gasto, descripcion, monto, 
               kilometraje, ruta, comprobante_numero, estado
        FROM Gastos
        WHERE id = ? AND conductor_id = ? AND estado = 'Pendiente'
    """, (gasto_id, session['user_id']))
    
    gasto = cursor.fetchone()
    
    if not gasto:
        flash('Gasto no encontrado o no se puede editar', 'warning')
        cursor.close()
        conn.close()
        return redirect(url_for('gastos'))
    
    if request.method == 'POST':
        fecha_gasto = request.form.get('fecha_gasto')
        tipo_gasto = request.form.get('tipo_gasto')
        descripcion = request.form.get('descripcion', '').strip()
        monto = request.form.get('monto', '0')
        kilometraje = request.form.get('kilometraje', '')
        ruta = request.form.get('ruta', '').strip()
        comprobante = request.form.get('comprobante_numero', '').strip()
        
        try:
            monto_float = float(monto)
            if monto_float <= 0:
                raise ValueError
            
            cursor.execute("""
                UPDATE Gastos
                SET fecha_gasto = ?, tipo_gasto = ?, descripcion = ?, 
                    monto = ?, kilometraje = ?, ruta = ?, comprobante_numero = ?
                WHERE id = ? AND conductor_id = ?
            """, (fecha_gasto, tipo_gasto, descripcion, monto_float, 
                  kilometraje or None, ruta, comprobante, gasto_id, session['user_id']))
            
            conn.commit()
            flash('Gasto actualizado exitosamente', 'success')
            cursor.close()
            conn.close()
            return redirect(url_for('gastos'))
            
        except Exception as e:
            flash(f'Error al actualizar: {str(e)}', 'danger')
            conn.rollback()
    
    cursor.close()
    conn.close()
    
    return render_template('editar_gasto.html', gasto=gasto)

@app.route('/eliminar-gasto/<int:gasto_id>', methods=['POST'])
@login_required
def eliminar_gasto(gasto_id):
    """Eliminar un gasto (solo si está pendiente)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            DELETE FROM Gastos
            WHERE id = ? AND conductor_id = ? AND estado = 'Pendiente'
        """, (gasto_id, session['user_id']))
        
        if cursor.rowcount > 0:
            conn.commit()
            flash('Gasto eliminado correctamente', 'success')
        else:
            flash('No se pudo eliminar el gasto', 'warning')
    except pyodbc.Error as e:
        flash(f'Error: {str(e)}', 'danger')
        conn.rollback()
    
    cursor.close()
    conn.close()
    return redirect(url_for('gastos'))

# ============================================
# RUTAS DE ADMINISTRACIÓN
# ============================================

@app.route('/admin/aprobar-gastos')
@admin_required
def aprobar_gastos():
    """Panel de aprobación de gastos (admin/supervisor)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Filtros
    estado = request.args.get('estado', 'Pendiente')
    conductor = request.args.get('conductor', '')
    
    query = """
        SELECT g.id, c.codigo_conductor, c.nombre, c.apellido,
               g.fecha_gasto, g.tipo_gasto, g.descripcion, g.monto,
               g.ruta, g.comprobante_numero, g.estado, g.fecha_registro
        FROM Gastos g
        INNER JOIN Conductores c ON g.conductor_id = c.id
        WHERE 1=1
    """
    params = []
    
    if estado and estado != 'Todos':
        query += " AND g.estado = ?"
        params.append(estado)
    if conductor:
        query += " AND (c.codigo_conductor LIKE ? OR c.nombre LIKE ? OR c.apellido LIKE ?)"
        params.extend([f'%{conductor}%', f'%{conductor}%', f'%{conductor}%'])
    
    query += " ORDER BY g.fecha_registro DESC"
    
    cursor.execute(query, params)
    gastos_pendientes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('admin_aprobar.html', 
                          gastos=gastos_pendientes,
                          filtros={'estado': estado, 'conductor': conductor})

@app.route('/admin/cambiar-estado/<int:gasto_id>', methods=['POST'])
@admin_required
def cambiar_estado_gasto(gasto_id):
    """Aprobar o rechazar un gasto"""
    nuevo_estado = request.form.get('estado')
    observaciones = request.form.get('observaciones', '').strip()
    
    if nuevo_estado not in ['Aprobado', 'Rechazado']:
        flash('Estado inválido', 'danger')
        return redirect(url_for('aprobar_gastos'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE Gastos
            SET estado = ?, aprobado_por = ?, fecha_aprobacion = GETDATE(), observaciones = ?
            WHERE id = ?
        """, (nuevo_estado, session['user_id'], observaciones, gasto_id))
        
        conn.commit()
        flash(f'Gasto {nuevo_estado.lower()} correctamente', 'success')
    except pyodbc.Error as e:
        flash(f'Error: {str(e)}', 'danger')
        conn.rollback()
    
    cursor.close()
    conn.close()
    return redirect(url_for('aprobar_gastos'))

@app.route('/admin/conductores')
@admin_required
def admin_conductores():
    """Lista de conductores (admin)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, codigo_conductor, nombre, apellido, email, telefono,
               empresa, placa_vehiculo, tipo_vehiculo, rol, activo, fecha_registro
        FROM Conductores
        ORDER BY fecha_registro DESC
    """)
    
    conductores = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin_conductores.html', conductores=conductores)

@app.route('/admin/reportes')
@admin_required
def admin_reportes():
    """Reportes y estadísticas (admin)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Resumen por conductor
    cursor.execute("""
        SELECT c.codigo_conductor, c.nombre, c.apellido,
               COUNT(g.id) as total_gastos,
               ISNULL(SUM(g.monto), 0) as total_monto,
               SUM(CASE WHEN g.estado = 'Pendiente' THEN 1 ELSE 0 END) as pendientes,
               SUM(CASE WHEN g.estado = 'Aprobado' THEN 1 ELSE 0 END) as aprobados
        FROM Conductores c
        LEFT JOIN Gastos g ON c.id = g.conductor_id
        WHERE c.rol = 'conductor' AND c.activo = 1
        GROUP BY c.codigo_conductor, c.nombre, c.apellido
        ORDER BY total_monto DESC
    """)
    resumen_conductores = cursor.fetchall()
    
    # Resumen por tipo de gasto
    cursor.execute("""
        SELECT tipo_gasto, 
               COUNT(*) as cantidad,
               SUM(monto) as total
        FROM Gastos
        GROUP BY tipo_gasto
        ORDER BY total DESC
    """)
    resumen_tipos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('admin_reportes.html',
                          resumen_conductores=resumen_conductores,
                          resumen_tipos=resumen_tipos)

# ============================================
# RUTAS API (JSON)
# ============================================

@app.route('/api/gastos/estadisticas')
@login_required
def api_estadisticas():
    """API para obtener estadísticas del conductor"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT estado, COUNT(*) as cantidad, SUM(monto) as total
        FROM Gastos
        WHERE conductor_id = ?
        GROUP BY estado
    """, (session['user_id'],))
    
    stats = {}
    for row in cursor.fetchall():
        stats[row[0]] = {
            'cantidad': row[1],
            'total': float(row[2]) if row[2] else 0
        }
    
    cursor.close()
    conn.close()
    
    return jsonify(stats)

# ============================================
# MANEJO DE ERRORES
# ============================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

# ============================================
# INICIALIZACIÓN
# ============================================

if __name__ == '__main__':
    print("=" * 60)
    print("Sistema de Legalización de Gastos para Conductores")
    print("=" * 60)
    
    # Inicializar base de datos
    print("\nInicializando base de datos...")
    if init_database():
        print("\n✅ Sistema listo para usar")
        print(f"\nServidor: http://localhost:5000")
        print(f"Usuario por defecto: ADMIN")
        print(f"Contraseña: admin123")
        print("\n" + "=" * 60)
        
        # Iniciar servidor
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("\n❌ Error al inicializar la base de datos")
        print("Verifica la configuración de SQL Server en SQL_CONFIG")
