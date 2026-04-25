
###### llamamos la libreria a trabajar
import pyodbc       ### Realiza conexion a la base de datos
import pandas as pd ### Lee los archivos
###import sqlite3 ###as SQLite
 
##### Informacion de la base de datos
server = '192.168.0.132'
dataBase = 'REPOSITORIO_MTTO'
userName = 'Odbc'
password = 'Odbc.2019'
#conexionString = 'DRIVER={{SQL Server}};SERVER={server};DATABASE={dataBase};Trusted_Connection=yes;'
#conexionString ='DRIVER={{SQL Server}};SERVER={server};DATABASE={dataBase};UID={userName};PWD={password}'
conexionString ='DRIVER={SQL Server};SERVER=192.168.0.132;DATABASE=REPOSITORIO_MTTO;UID=Odbc;PWD=Odbc.2019'
 
try:
    conexion = pyodbc.connect(conexionString)
    print('Conexion Exitosa')
except:
    print('Error en conexion')
   

#### Ejecutamos la Información y la guardamos en la memoria
cursor = conexion.cursor()


#### Llamamos la base de Datos 
query_Vehiculo = "SELECT * FROM dbo.Tb_CloudFleet_001_Vehiculos"


#### Leemos la tabla mediante la libreria pandas y la nombramos df_tablas
df_tablas = pd.read_sql(query_Vehiculo,conexion)

df_tablas.head()
#### Convertimos la informacion a una dataframe y verificamos la información. 
df_tablas.info()

#### Llamos las cinco primeras filas
df_tablas.sample(1)
