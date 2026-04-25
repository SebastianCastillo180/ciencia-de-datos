
import pyodbc       ### Realiza conexion a la base de datos
import pandas as pd ### Lee los archivos
### import sqlite3 as SQLite
import numpy as np
 
##### Informacion de la base de datos
server = '192.168.0.133'
dataBase = 'DataLake'
userName = 'siesarayo'
password = 'SisR@yos.2017'
#conexionString = 'DRIVER={{SQL Server}};SERVER={server};DATABASE={dataBase};Trusted_Connection=yes;'
#conexionString = 'DRIVER={{SQL Server}};SERVER={server};DATABASE={dataBase};UID={userName};PWD={password}'
conexionString ='DRIVER={SQL Server};SERVER=192.168.0.133;DATABASE=DataLake;UID=siesarayo;PWD=SisR@yos.2017'
 
try:
    conexion = pyodbc.connect(conexionString)
    print('Conexion Exitosa')
except:
    print('Error en conexion')
   

#### Ejecutamos la Información y la guardamos en la memoria
cursor = conexion.cursor()


#### Llamamos la base de Datos 
query_Viaje = "SELECT * FROM get.Viaje"


#### Leemos la tabla mediante la libreria pandas y la nombramos df_tablas
df_Tabla = pd.read_sql(query_Viaje,conexion)

#### Convertimos la informacion a una dataframe y verificamos la información. 
print(df_Tabla)

----------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------

import json
import pyodbc

# --- 1. Configuración de la conexión a SQL Server ---
# Reemplaza con tus propios datos
server = 'nombre_del_servidor'  # Ej: 'MI-PC\SQLEXPRESS' o la IP del servidor
database = 'nombre_de_la_base_de_datos'
username = 'tu_usuario'
password = 'tu_contraseña'

# Cadena de conexión (ConnectionString)
# Se usa 'ODBC Driver 17 for SQL Server' que es el más común y recomendado.
# Asegúrate de tener el driver instalado.
try:
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
    )
    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()
    print("¡Conexión exitosa a SQL Server! ✅")

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"Error de conexión: {sqlstate}. Verifica tus datos y el driver.")
    exit()


# --- 2. Cargar datos del archivo JSON ---
try:
    with open('datos.json', 'r') as archivo_json:
        datos = json.load(archivo_json)
    print(f"Se cargaron {len(datos)} registros del archivo JSON.")

except FileNotFoundError:
    print("Error: El archivo 'datos.json' no se encontró. 😕")
    exit()
except json.JSONDecodeError:
    print("Error: El archivo JSON tiene un formato incorrecto.")
    exit()


# --- 3. Insertar los datos en SQL Server ---
try:
    for registro in datos:
        # Consulta SQL para insertar los datos
        # Se usan '?' como marcadores de posición para evitar inyección SQL
        sql_insert_query = """
            INSERT INTO Usuarios (Nombre, Edad, Ciudad)
            VALUES (?, ?, ?);
        """
        
        # Ejecutar la consulta con los valores del registro actual
        cursor.execute(sql_insert_query, registro['nombre'], registro['edad'], registro['ciudad'])

    # Confirmar la transacción para guardar los cambios en la base de datos
    cnxn.commit()
    print(f"¡Se han insertado {cursor.rowcount} registros exitosamente en la tabla Usuarios! 🎉")

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"Error al insertar datos: {sqlstate}")
    # Si hay un error, revertir los cambios
    cnxn.rollback()

finally:
    # --- 4. Cerrar la conexión ---
    if 'cnxn' in locals() and cnxn:
        cursor.close()
        cnxn.close()
        print("La conexión a la base de datos se ha cerrado.")

