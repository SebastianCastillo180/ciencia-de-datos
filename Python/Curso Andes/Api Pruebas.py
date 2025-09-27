

import requests
import json

# URL base del servicio REST
base_url = "https://fleet.cloudfleet.com/api/v1/vehicles/"

# Token de autorización
token = "1mT6Lny.R38_jSB5iTHtmUKD2d6RdOXQZDD8HLzg4"

# Headers de la petición
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",
}

# Inicializar la página en 1
page = 1

# Inicializar una lista para almacenar todas las respuestas
all_data = []

while True:
    # Agregar el parámetro de página a la URL
    url = f"{base_url}?page={page}"

    # Realizar la petición GET
    response = requests.get(url, headers=headers)

    # Verificar que la petición fue exitosa
    if response.status_code == 200:
        # Convertir la respuesta a JSON
        data = response.json()

        # Verificar si el mensaje de error está en la respuesta
        if "error" in data and data["error"]["message"] == "No Vehicles found with the specified filters":
            break

        # Agregar la respuesta a la lista
        all_data.append(data)

        # Incrementar la página
        page += 1
    else:
        print(f"Error: {response.status_code}")
        break

# Guardar todas las respuestas en un archivo .json
with open("ListarVehiculos.json", "w") as file:
    json.dump(all_data, file, indent=4)




# Se lee la respuestas en un archivo .json
data
for DF2 in data:
    print(DF2)
    
    
BD = pd.DataFrame(DF2)

BD.head()

import json, os
import pandas as pd



BD = pd.DataFrame(data)

BD

"""
################################### Segundo Paso ########################
# Importamos la libreria pandas para leer el archivo
import pandas as pd

# Convertimos el archivo en un dataframe o datos estructurados. 
BD = pd.DataFrame(data)

BD.info()

################################### Tercer Paso #########################

###### llamamos la libreria a trabajar
import pyodbc       ### Realiza conexion a la base de datos
import pandas as pd ### Lee los archivos
import sqlite3 as SQLite
 
##### Informacion de la base de datos
server = '192.168.0.139\BODEGA'
dataBase = 'DataStage'
userName = 'Odbc'
password = 'Odbc.2019'
#conexionString = 'DRIVER={{SQL Server}};SERVER={server};DATABASE={dataBase};Trusted_Connection=yes;'
#conexionString ='DRIVER={{SQL Server}};SERVER={server};DATABASE={dataBase};UID={userName};PWD={password}'
conexionString ='DRIVER={SQL Server};SERVER=192.168.0.139\BODEGA;DATABASE=DataStage;UID=Odbc;PWD=Odbc.2019'
 
try:
    conexion = pyodbc.connect(conexionString)
    print('Conexion Exitosa')
except:
    print('Error en conexion')
   

#### Ejecutamos la Información y la guardamos en la memoria
cursor = conexion.cursor()


conexion.close()

"""