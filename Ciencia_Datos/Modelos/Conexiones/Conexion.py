# Importa las biblioteca
import pyodbc   #### Esta Libreria 
import pandas as pd
import numpy as np

BD = pd.DataFrame({"Manzana": [3,2], "Peras" : [1,4]}, index=["Juan","Pedro"])
print(BD)

import matplotlib

BD.plot.bar()

### Leer atchivos en formato csv
csv = pd.read_csv("Ventas_Abril24.csv")


### Leer atchivos en formato excel
###df_excel = pd.read_excel("Ventas_Abril24.xlsx")


# Configura la conexión a la base de datos
server = '192.168.0.139'
database = 'DataStage'
username = 'sa'
password = 'T3mq%2023+ab1'
driver = '{ODBC Driver 17 for SQL Server}'