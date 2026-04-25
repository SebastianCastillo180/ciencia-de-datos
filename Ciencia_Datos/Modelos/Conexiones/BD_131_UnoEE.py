#### https://project2080.com/como-conectar-python-con-sql-server/


###### llamamos la libreria a trabajar
import pyodbc       ### Realiza conexion a la base de datos
import pandas as pd ### Lee los archivos
###import sqlite3 ###as SQLite
 
##### Información de la base de datos
server = '192.168.0.131'
dataBase = 'UnoEE'
userName = 'Odbc'
password = 'Odbc.2019'
#conexionString = 'DRIVER={{SQL Server}};SERVER={server};DATABASE={dataBase};Trusted_Connection=yes;'
#conexionString ='DRIVER={{SQL Server}};SERVER={server};DATABASE={dataBase};UID={userName};PWD={password}'
conexionString ='DRIVER={SQL Server};SERVER=192.168.0.131;DATABASE=UnoEE;UID=Odbc;PWD=Odbc.2019'
 
try:
    conexion = pyodbc.connect(conexionString)
    print('Conexion Exitosa')
except:
    print('Error en conexion')
   

#### Ejecutamos la Información y la guardamos en la memoria
cursor = conexion.cursor()


#### Llamamos la base de Datos 
query_Ventas = "SELECT * FROM dbo.t016_mm_bancos"

query_Nomina = "SELECT * FROM dbo.Ry_wv_Nomina"


#### Leemos la tabla mediante la libreria pandas y la nombramos df_tablas
df_Tabla = pd.read_sql(query_Ventas,conexion)
df_TablaN = pd.read_sql(query_Nomina,conexion)

#### Convertimos la informacion a una dataframe y verificamos la información. 
df_Tabla.info()

#### Descripción de los Datos 
df_Tabla.describe()

#### Llamos las cinco primeras filas
df_Tabla.head()
df_TablaN.head()

df_TablaN.describe()


df_Tabla.corr(numeric_only=True).abs()[["TOTAL A PAGAR"]]


##################################### Analisis Descriptivo #####################################

conexion.close()
