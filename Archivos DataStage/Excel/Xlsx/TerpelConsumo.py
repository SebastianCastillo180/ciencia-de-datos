
# pip install pandas openpyxl sqlalchemy pyodbc
# pip install pandas sqlalchemy pyodbc openpyxl


import pandas as pd
import urllib  # Se importa de forma independiente
from sqlalchemy import create_engine

# 1. Configuración de la ruta y credenciales
file_path = r'D:\Rayogas\Sistemas de Informacion - Estrategia de Datos\7. Fuentes de Informacion\Xls\Mantenimiento\Terpel\Consumo Terpel 2026.xlsx'






server = '192.168.0.133' # Asegúrate de completar los octetos faltantes
database = 'DataLake'
schema = 'xls'
username = 'siesarayo'
password = 'SisR@yos.2017'

try:
    # 2. Leer el archivo Excel
    df = pd.read_excel(file_path)
    print("Archivo Excel leído exitosamente.")

    # 3. Configurar la conexión a SQL Server
    # Corregimos la cadena usando urllib.parse.quote_plus
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password}"
    )
    quoted_conn_str = urllib.parse.quote_plus(conn_str)
    
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={quoted_conn_str}")

    # 4. Insertar datos
    table_name = 'Ventas_Terpel_API'
    df.to_sql(name=table_name, 
              con=engine, 
              schema=schema, 
              if_exists='replace', 
              index=False)

    print(f"Éxito: Datos insertados en {database}.{schema}.{table_name}")

except Exception as e:
    print(f"Ocurrió un error: {e}")