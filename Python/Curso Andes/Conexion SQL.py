# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:16:30 2024

@author: analistabi
"""

#### https://project2080.com/como-conectar-python-con-sql-server/


#### https://www.youtube.com/watch?v=5rS7TtlmNWM


import pyodbc       ### Realiza conexion a la base de datos
import pandas as pd ### Lee los archivos
import sqlite3 as SQLite
 
##### Informacion de la base de datos
server = '192.168.0.132'
dataBase = 'DataStage'
userName = 'Odbc'
password = 'Odbc.2019'
#conexionString = 'DRIVER={{SQL Server}};SERVER={server};DATABASE={dataBase};Trusted_Connection=yes;'
#conexionString = 'DRIVER={{SQL Server}};SERVER={server};DATABASE={dataBase};UID={userName};PWD={password}'
conexionString ='DRIVER={SQL Server};SERVER=192.168.0.132;DATABASE=DataStage;UID=Odbc;PWD=Odbc.2019'
 
try:
    conexion = pyodbc.connect(conexionString)
    print('Conexion Exitosa')
except:
    print('Error en conexion')
   

#### Ejecutamos la Información y la guardamos en la memoria
cursor = conexion.cursor()

##query_Claro = "SELECT movil FROM xls.LineasRayogas WHERE  Valor IS NULL"

#### Leemos la tabla mediante la libreria pandas y la nombramos df_tablas
##df_tablas = pd.read_sql(query_Claro,conexion)

##df_tablas.head(3)

##############################################################################################################
############################# Segundo Paso Inserción de Datos a SQL ##########################################
# Importamos la libreria pandas
import pandas as pd

# llamamos nuestro archivo en format cvs
Variables = pd.read_excel(r"C:\Users\analistabi\Downloads\Corredores.xlsx") 
Variables
# convertimos nuestro data set en lista
VariablesLista = Variables.values.tolist()
VariablesLista

# Creamos la tabla 
cursor.execute("CREATE TABLE CiudadesPruE(Ciudad FLOAT, Pais VARCHAR(100) NOT NULL, PRIMARY KEY (Pais))")


# Insertamos los datos en la tabla Ciudad y nuestra lista variable
cursor.executemany("INSERT INTO CiudadesPru VALUES(?,?)", VariablesLista)

# Este codigo envia la información a nuestra base de datos
cursor.commit()

#Nos aseguramos de cerrar la conexión
conexion.close()