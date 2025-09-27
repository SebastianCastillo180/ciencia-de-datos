# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 11:52:16 2024

@author: analistabi
"""



import pyodbc
import pandas as pd
# insert data from csv file into dataframe.
# working directory for csv file: type "pwd" in Azure Data Studio or Linux
# working directory in Windows c:\users\username
Variables = pd.read_csv(r"C:\Users\analistabi\Downloads\Corredores.csv")
Variables.head()


## Convertimos en una lista
VariablesLista = Variables.values.tolist()
VariablesLista


### Conexion Base de datos
server = 'SVRV-BD2' 
bd = 'DataStage' 


conexion = pyodbc.connect(driver='{SQL server}', host = server, databases = bd)
print('Conexion Exitosa')


cursor = conexion.cursor()


cursor.execute("CREATE TABLE CiudadesPruE(Corredor  INTEGER, Lugar  INTEGER, Genero VARCHAR(25), Edad INTEGER, Pais VARCHAR(255), Tiempo FLOAT, PRIMARY KEY (Corredor))")


# Insertamos los datos en la tabla Ciudad y nuestra lista variable
cursor.executemany("INSERT INTO CiudadesPruE VALUES(?,?,?,?,?,?)", VariablesLista)

# Este codigo envia la información a nuestra base de datos
cursor.commit()

#Nos aseguramos de cerrar la conexión
conexion.close()



