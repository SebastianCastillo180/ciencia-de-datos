"""
Archivo de Configuración - Sistema de Legalización de Gastos
"""

class Config:
    """Configuración de la base de datos SQL Server"""
    
    # Configuración del servidor SQL Server
    SQL_SERVER = '192.168.0.22'
    SQL_DATABASE = 'GastosDB'
    SQL_USERNAME = 'sa'  # Cambiar por tu usuario de SQL Server
    SQL_PASSWORD = 'TuPassword123!'  # IMPORTANTE: Cambiar por tu contraseña
    
    # Driver ODBC (prueba en este orden si uno no funciona)
    # Opción 1: Driver más reciente
    SQL_DRIVER = 'ODBC Driver 17 for SQL Server'
    
    # Opción 2: Si el Driver 17 no está disponible
    # SQL_DRIVER = 'ODBC Driver 13 for SQL Server'
    
    # Opción 3: Driver más antiguo pero común
    # SQL_DRIVER = 'SQL Server'
    
    # Timeout de conexión (segundos)
    CONNECTION_TIMEOUT = 10
    
    # Configuración de la aplicación
    APP_TITLE = 'Sistema de Legalización de Gastos'
    APP_VERSION = '2.0 - SQL Server Edition'
    
    # Configuración de seguridad
    MIN_PASSWORD_LENGTH = 6
    PASSWORD_REQUIRES_NUMBER = False
    PASSWORD_REQUIRES_SPECIAL = False
    
    # Configuración de interfaz
    THEME_PRIMARY = '#3498db'
    THEME_SUCCESS = '#27ae60'
    THEME_DANGER = '#e74c3c'
    THEME_WARNING = '#f39c12'
    THEME_DARK = '#2c3e50'
    THEME_LIGHT = '#ecf0f1'
    
    # Categorías de gastos
    CATEGORIAS = [
        'Transporte',
        'Alimentación',
        'Hospedaje',
        'Material',
        'Servicios',
        'Capacitación',
        'Tecnología',
        'Otros'
    ]
    
    # Estados de gastos
    ESTADOS = {
        'PENDIENTE': 'Pendiente',
        'APROBADO': 'Aprobado',
        'RECHAZADO': 'Rechazado',
        'CANCELADO': 'Cancelado'
    }
    
    # Roles de usuario
    ROLES = {
        'ADMIN': 'admin',
        'SUPERVISOR': 'supervisor',
        'USUARIO': 'usuario'
    }
    
    @staticmethod
    def get_connection_string():
        """Genera la cadena de conexión completa"""
        return (
            f'DRIVER={{{Config.SQL_DRIVER}}};'
            f'SERVER={Config.SQL_SERVER};'
            f'DATABASE={Config.SQL_DATABASE};'
            f'UID={Config.SQL_USERNAME};'
            f'PWD={Config.SQL_PASSWORD};'
            f'Connection Timeout={Config.CONNECTION_TIMEOUT};'
        )
    
    @staticmethod
    def get_connection_string_windows_auth():
        """Genera cadena de conexión con autenticación de Windows"""
        return (
            f'DRIVER={{{Config.SQL_DRIVER}}};'
            f'SERVER={Config.SQL_SERVER};'
            f'DATABASE={Config.SQL_DATABASE};'
            f'Trusted_Connection=yes;'
            f'Connection Timeout={Config.CONNECTION_TIMEOUT};'
        )


# Función auxiliar para probar la conexión
def test_connection():
    """Prueba la conexión a SQL Server"""
    import pyodbc
    
    print("=" * 50)
    print("Probando conexión a SQL Server...")
    print("=" * 50)
    
    try:
        # Intentar con autenticación SQL
        print(f"\n1. Probando con usuario SQL: {Config.SQL_USERNAME}")
        conn_string = Config.get_connection_string()
        conn = pyodbc.connect(conn_string)
        print("✅ Conexión exitosa con autenticación SQL")
        conn.close()
        return True
        
    except pyodbc.Error as e:
        print(f"❌ Error con autenticación SQL: {e}")
        
        try:
            # Intentar con autenticación Windows
            print("\n2. Probando con autenticación Windows...")
            conn_string = Config.get_connection_string_windows_auth()
            conn = pyodbc.connect(conn_string)
            print("✅ Conexión exitosa con autenticación Windows")
            conn.close()
            return True
            
        except pyodbc.Error as e2:
            print(f"❌ Error con autenticación Windows: {e2}")
            print("\n" + "=" * 50)
            print("SOLUCIONES POSIBLES:")
            print("=" * 50)
            print("1. Verificar que SQL Server esté corriendo")
            print("2. Verificar usuario y contraseña en config.py")
            print("3. Verificar que el puerto 1433 esté abierto")
            print("4. Instalar driver ODBC correcto")
            print("5. Verificar firewall de Windows")
            return False


if __name__ == "__main__":
    # Ejecutar prueba de conexión
    test_connection()
