"""
Configuración de conexión a Base de Datos
IMPORTANTE: Actualice estos valores con sus credenciales
"""

# MODO DE BASE DE DATOS
# 'sqlite' = Usar SQLite local (temporal, mientras se resuelve problema de red)
# 'sqlserver' = Usar SQL Server remoto
MODO_BD = 'sqlite'  # ← CAMBIAR A 'sqlserver' cuando el servidor sea accesible

# Configuración de SQL Server
SQL_SERVER_CONFIG = {
    'server': '192.155.0.22',
    'port': 1433,  # Puerto de SQL Server (por defecto 1433)
    'database': 'Replica',
    'username': 'siesarayo',
    'password': 'SisR@yos.2017',
    'driver': '{SQL Server}',  # Cambiado a driver simple. Alternativas: '{ODBC Driver 17 for SQL Server}', '{ODBC Driver 13 for SQL Server}'
    'trusted_connection': False,
    'timeout': 30  # Timeout en segundos
}

def get_connection_string():
    """Genera la cadena de conexión para SQL Server"""
    server = SQL_SERVER_CONFIG['server']
    port = SQL_SERVER_CONFIG.get('port', 1433)

    # Agregar puerto si no está en el servidor
    if ':' not in server and ',' not in server:
        server_with_port = f"{server},{port}"
    else:
        server_with_port = server

    if SQL_SERVER_CONFIG['trusted_connection']:
        # Autenticación de Windows
        return (
            f"DRIVER={SQL_SERVER_CONFIG['driver']};"
            f"SERVER={server_with_port};"
            f"DATABASE={SQL_SERVER_CONFIG['database']};"
            f"Trusted_Connection=yes;"
            f"Connection Timeout={SQL_SERVER_CONFIG.get('timeout', 30)};"
        )
    else:
        # Autenticación SQL Server
        return (
            f"DRIVER={SQL_SERVER_CONFIG['driver']};"
            f"SERVER={server_with_port};"
            f"DATABASE={SQL_SERVER_CONFIG['database']};"
            f"UID={SQL_SERVER_CONFIG['username']};"
            f"PWD={SQL_SERVER_CONFIG['password']};"
            f"Connection Timeout={SQL_SERVER_CONFIG.get('timeout', 30)};"
        )
