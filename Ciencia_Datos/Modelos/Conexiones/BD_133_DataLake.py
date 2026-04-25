#### https://project2080.com/como-conectar-python-con-sql-server/


###### llamamos la libreria a trabajar
import pyodbc       ### Realiza conexion a la base de datos
import pandas as pd ### Lee los archivos
###import sqlite3 ###as SQLite
 
##### Informacion de la base de datos
server = '192.168.0.139\BODEGA'
dataBase = 'DataLake'
userName = 'PBI'
password = 'Rayo.2026-*'
#conexionString = 'DRIVER={{SQL Server}};SERVER={server};DATABASE={dataBase};Trusted_Connection=yes;'
#conexionString ='DRIVER={{SQL Server}};SERVER={server};DATABASE={dataBase};UID={userName};PWD={password}'
conexionString ='DRIVER = {SQL Server}; SERVER = 192.168.0.133\BODEGA; DATABASE = DataLake; UID = PBI ; PWD = Rayo.2026-*'
 
try:
    conexion = pyodbc.connect(conexionString)
    print('Conexion Exitosa')
except:
    print('Error en conexion')
   

#### Ejecutamos la Información y la guardamos en la memoria
cursor = conexion.cursor()


#### Llamamos la base de Datos 
query_Mov = "SELECT * FROM [app].[AccidenteLaboral]"


####query_Mov = "SELECT * FROM  WHERE  Valor IS NULL"


#### Leemos la tabla mediante la libreria pandas y la nombramos df_tablas
df_Mov = pd.read_sql(query_Mov,conexion)
df_Mov.head(3)

#### Convertimos la informacion a una dataframe y verificamos la información. 
df_Mov.info()

#### Llamos las cinco primeras filas
##df_tablas.sample(1)

##numero = df_tablas.sample(1)

##numero



cursor.execute("CREATE TABLE Ciudad(Ciudad VARCHAR(255) NOT NULL, Pais VARCHAR(100) NOT NULL, PRIMARY KEY (Ciudad))")


#Creamos una lista de Ciudades y sus paises 
Variables = [
            ('Bogota','Colombia'),
            ('Buenos Aires','Argentina'),
            ('Caracas','Venezuela')
]

#Insertamos los datos en la tabla Ciudad
cursor.executemany("INSERT INTO Ciudad VALUES(?,?)", Variables)


conexion.close()