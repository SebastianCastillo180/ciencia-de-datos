
#### https://www.youtube.com/watch?v=5rS7TtlmNWM


import pyodbc       ### Realiza conexion a la base de datos
import pandas as pd ### Lee los archivos
import sqlite3 as SQLite
 
##### Informacion de la base de datos
server = 'SVRV-BD2'
dataBase = 'DataStage'
userName = 'Odbc'
password = 'Odbc.2019'
#conexionString = 'DRIVER={{SQL Server}};SERVER={server};DATABASE={dataBase};Trusted_Connection=yes;'
#conexionString = 'DRIVER={{SQL Server}};SERVER={server};DATABASE={dataBase};UID={userName};PWD={password}'
conexionString ='DRIVER={SQL Server};SERVER=SVRV-BD2;DATABASE=DataStage;UID=Odbc;PWD=Odbc.2019'
 
try:
    conexion = pyodbc.connect(conexionString)
    print('Conexion Exitosa')
except:
    print('Error en conexion')
   

#### Ejecutamos la Información y la guardamos en la memoria
cursor = conexion.cursor()

###query_Claro = "SELECT movil FROM xls.LineasRayogas WHERE  Valor IS NULL"

#### Leemos la tabla mediante la libreria pandas y la nombramos df_tablas
##df_tablas = pd.read_sql(query_Claro,conexion)

##df_tablas.head(3)

##############################################################################################################
############################# Segundo Paso Inserción de Datos a SQL ##########################################
# Importamos la libreria pandas
import pandas as pd
####pip install openpyxl
import openpyxl

# llamamos nuestro archivo en format cvs
Variables = pd.read_excel(r"C:\Users\analistabi\Downloads\GLPS.xlsx") 

# convertimos nuestro data set en lista
VariablesLista = Variables.values.tolist()
VariablesLista

# Creamos la tabla 
cursor.execute("CREATE TABLE CiudadesPruebasV2(Ciudad VARCHAR(255), Pais VARCHAR(100), Dinero float, Fecha DATE, PRIMARY KEY (Ciudad))")


# Insertamos los datos en la tabla Ciudad y nuestra lista variable
cursor.executemany("INSERT INTO CiudadesPruebasV2 VALUES(?,?,?,?)", VariablesLista)

# Este codigo envia la información a nuestra base de datos
cursor.commit()

#Nos aseguramos de cerrar la conexión
conexion.close()