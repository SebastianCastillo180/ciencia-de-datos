
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

################################################### Parte # 4 ##########################################
########################################################################################################

# Creamos la tabla 
##cursor.execute("CREATE TABLE Ciudades(Ciudad VARCHAR(255) NOT NULL, Pais VARCHAR(100) NOT NULL, PRIMARY KEY (Ciudad))")

cursor.execute("CREATE TABLE AVehiculos(id VARCHAR(255) NOT NULL, code VARCHAR(255) NOT NULL, typeName VARCHAR(255) NOT NULL, brandName VARCHAR(255) NOT NULL, lineName VARCHAR(255) NOT NULL, odometerType VARCHAR(255) NOT NULL, mainMeasurementType VARCHAR(255) NOT NULL, odometer VARCHAR(255) NOT NULL, hourmeter VARCHAR(255) NOT NULL, year VARCHAR(255) NOT NULL, color VARCHAR(255) NOT NULL, mainFuelType VARCHAR(255) NOT NULL, auxFuelType VARCHAR(255) NOT NULL, workload VARCHAR(255) NOT NULL, maxOdometerDay VARCHAR(255) NOT NULL, avgOdometerDay VARCHAR(255) NOT NULL, maxHourmeterDay VARCHAR(255) NOT NULL, avgHourmeterDay VARCHAR(255) NOT NULL, city VARCHAR(255) NOT NULL, costCenter VARCHAR(255) NOT NULL, group1 VARCHAR(255) NOT NULL, group2 VARCHAR(255) NOT NULL, commentGroupingData VARCHAR(255) NOT NULL, auxCode VARCHAR(255) NOT NULL, vin VARCHAR(255) NOT NULL, imeiGps VARCHAR(255) NOT NULL, owner VARCHAR(255) NOT NULL, engine VARCHAR(255) NOT NULL, weightCapacity VARCHAR(255) NOT NULL, chassisNumber VARCHAR(255) NOT NULL, serialNumber VARCHAR(255) NOT NULL, purchaseDate VARCHAR(255) NOT NULL, purchaseOdometer VARCHAR(255) NOT NULL, purchaseHourmeter VARCHAR(255) NOT NULL, purchasePrice VARCHAR(255) NOT NULL, seller VARCHAR(255) NOT NULL, subaccountQty VARCHAR(255) NOT NULL, driver VARCHAR(255) NOT NULL, createdAt VARCHAR(255) NOT NULL, createdBy VARCHAR(255) NOT NULL)")


# Insertamos los datos en la tabla Ciudad y nuestra lista variable
cursor.executemany("INSERT INTO AVehiculos VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", ListVehiculos)

# Este codigo envia la información a nuestra base de datos
cursor.commit()

#Nos aseguramos de cerrar la conexión
conexion.close()































# Creamos la tabla 
##cursor.execute("CREATE TABLE Ciudades(Ciudad VARCHAR(255) NOT NULL, Pais VARCHAR(100) NOT NULL, PRIMARY KEY (Ciudad))")

cursor.execute("CREATE TABLE AVehiculos(id VARCHAR(255) NOT NULL, code VARCHAR(255) NOT NULL, typeName VARCHAR(255) NOT NULL, brandName VARCHAR(255) NOT NULL, lineName VARCHAR(255) NOT NULL, odometerType VARCHAR(255) NOT NULL, mainMeasurementType VARCHAR(255) NOT NULL, odometer VARCHAR(255) NOT NULL, hourmeter VARCHAR(255) NOT NULL, year VARCHAR(255) NOT NULL, color VARCHAR(255) NOT NULL, mainFuelType VARCHAR(255) NOT NULL, auxFuelType VARCHAR(255) NOT NULL, workload VARCHAR(255) NOT NULL, maxOdometerDay VARCHAR(255) NOT NULL, avgOdometerDay VARCHAR(255) NOT NULL, maxHourmeterDay VARCHAR(255) NOT NULL, avgHourmeterDay VARCHAR(255) NOT NULL, city VARCHAR(255) NOT NULL, costCenter VARCHAR(255) NOT NULL, group1 VARCHAR(255) NOT NULL, group2 VARCHAR(255) NOT NULL, commentGroupingData VARCHAR(255) NOT NULL, auxCode VARCHAR(255) NOT NULL, vin VARCHAR(255) NOT NULL, imeiGps VARCHAR(255) NOT NULL, owner VARCHAR(255) NOT NULL, engine VARCHAR(255) NOT NULL, weightCapacity VARCHAR(255) NOT NULL, chassisNumber VARCHAR(255) NOT NULL, serialNumber VARCHAR(255) NOT NULL, purchaseDate VARCHAR(255) NOT NULL, purchaseOdometer VARCHAR(255) NOT NULL, purchaseHourmeter VARCHAR(255) NOT NULL, purchasePrice VARCHAR(255) NOT NULL, seller VARCHAR(255) NOT NULL, subaccountQty VARCHAR(255) NOT NULL, driver VARCHAR(255) NOT NULL, createdAt VARCHAR(255) NOT NULL, createdBy VARCHAR(255) NOT NULL)")


# Insertamos los datos en la tabla Ciudad y nuestra lista variable
cursor.executemany("INSERT INTO AVehiculos VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", ListVehiculos)

# Este codigo envia la información a nuestra base de datos
cursor.commit()

#Nos aseguramos de cerrar la conexión
conexion.close()