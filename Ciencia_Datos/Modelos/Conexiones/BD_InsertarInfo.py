
# Instalar el paquete pip intall pyodbc

############################# Primer Parte Conexion Base de Datos ##########################
import pyodbc       ### Realiza conexion a la base de datos
import pandas as pd ### Lee los archivos
import sqlite3 as SQLite
 
##### Informacion de la base de datos
server = '192.168.0.139\BODEGA'
dataBase = 'DataStage'
userName = 'Odbc'
password = 'Odbc.2019'
#conexionString = 'DRIVER={{SQL Server}};SERVER={server};DATABASE={dataBase};Trusted_Connection=yes;'
#conexionString = 'DRIVER={{SQL Server}};SERVER={server};DATABASE={dataBase};UID={userName};PWD={password}'
conexionString ='DRIVER={SQL Server};SERVER=192.168.0.139\BODEGA;DATABASE=DataStage;UID=Odbc;PWD=Odbc.2019'
 
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

# Creamos la tabla 
cursor.execute("CREATE TABLE APruebas(Nombre VARCHAR(255) NOT NULL, Apellido VARCHAR(100) NOT NULL, PRIMARY KEY (Nombre))")

# Creamos una lista de Ciudades y sus paises 
Variables = [
            ('Luis','Castro'),
            ('Jorge','Pitter'),
            ('Hamilton','Lopez')
]

# Insertamos los datos en la tabla Ciudad
cursor.executemany("INSERT INTO APruebas VALUES(?,?)", Variables)

# Este codigo envia la información a nuestra base de datos
cursor.commit()

#Nos aseguramos de cerrar la conexión
conexion.close()