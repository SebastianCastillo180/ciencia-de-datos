"""
Script para probar la conexión a SQL Server
Ayuda a diagnosticar problemas de conexión
"""

import pyodbc
from config_db import SQL_SERVER_CONFIG, get_connection_string

print("=" * 60)
print("PRUEBA DE CONEXIÓN A SQL SERVER")
print("=" * 60)
print()

print("Configuración actual:")
print(f"  Servidor: {SQL_SERVER_CONFIG['192.168.0.22']}")
print(f"  Base de datos: {SQL_SERVER_CONFIG['Replica']}")
print(f"  Usuario: {SQL_SERVER_CONFIG['siesarayo']}")
print(f"  Driver: {SQL_SERVER_CONFIG['driver']}")
print()

print("Cadena de conexión:")
conn_string = get_connection_string()
# Ocultar contraseña en la salida
conn_string_safe = conn_string.replace(SQL_SERVER_CONFIG['SisR@yos.2017'], '****')
print(f"  {conn_string_safe}")
print()

print("Drivers ODBC disponibles:")
drivers = [x for x in pyodbc.drivers()]
for i, driver in enumerate(drivers, 1):
    print(f"  {i}. {driver}")
print()

print("Intentando conectar al servidor SQL Server...")
print("(Esto puede tardar hasta 30 segundos)")
print()

try:
    conn = pyodbc.connect(conn_string, timeout=30)
    print("✓ ¡CONEXIÓN EXITOSA!")
    print()

    cursor = conn.cursor()

    # Probar consulta simple
    cursor.execute("SELECT @@VERSION")
    version = cursor.fetchone()[0]
    print("Versión de SQL Server:")
    print(f"  {version[:80]}...")
    print()

    # Listar tablas
    cursor.execute("""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
    """)

    tables = cursor.fetchall()
    print(f"Tablas en la base de datos '{SQL_SERVER_CONFIG['database']}':")
    if tables:
        for table in tables[:10]:  # Mostrar solo las primeras 10
            print(f"  - {table[0]}")
        if len(tables) > 10:
            print(f"  ... y {len(tables) - 10} tablas más")
    else:
        print("  (No hay tablas)")

    conn.close()
    print()
    print("=" * 60)
    print("La conexión funciona correctamente.")
    print("Puede ejecutar la aplicación sin problemas.")
    print("=" * 60)

except pyodbc.Error as e:
    print("✗ ERROR DE CONEXIÓN")
    print()
    print("Detalles del error:")
    print(f"  {str(e)}")
    print()
    print("POSIBLES SOLUCIONES:")
    print()
    print("1. Verificar que el servidor SQL Server esté en línea:")
    print(f"   - Ping al servidor: ping {SQL_SERVER_CONFIG['server']}")
    print()
    print("2. Verificar que SQL Server permita conexiones remotas:")
    print("   - SQL Server Configuration Manager")
    print("   - SQL Server Network Configuration > Protocols")
    print("   - Habilitar TCP/IP")
    print()
    print("3. Verificar el firewall:")
    print("   - Puerto 1433 debe estar abierto")
    print("   - Permitir SQL Server en el firewall de Windows")
    print()
    print("4. Verificar credenciales:")
    print("   - Usuario y contraseña correctos")
    print("   - El usuario tiene permisos en la base de datos")
    print()
    print("5. Probar con otro driver ODBC:")
    print("   - Cambiar en config_db.py:")
    print("   - 'driver': '{SQL Server}'")
    print("   - o 'driver': '{ODBC Driver 13 for SQL Server}'")
    print()
    print("6. Verificar el nombre/IP del servidor:")
    print(f"   - Servidor actual: {SQL_SERVER_CONFIG['server']}")
    print("   - Probar con: localhost, 127.0.0.1, o IP completa")
    print()
    print("=" * 60)

except Exception as e:
    print("✗ ERROR INESPERADO")
    print(f"  {str(e)}")
    print()

input("\nPresione Enter para salir...")
