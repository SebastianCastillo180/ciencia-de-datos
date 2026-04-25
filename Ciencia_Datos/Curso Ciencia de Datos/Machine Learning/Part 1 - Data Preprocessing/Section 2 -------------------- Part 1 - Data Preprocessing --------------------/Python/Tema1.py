# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
## Importamos librerias
import numpy as np
import matplotlib as plt
import pandas as pd

# Importamos el data set
dataset = pd.read_csv('DataML.csv')

## Identificamos mi variable pregunta (Y), mis variables dependientes (X)
# iloc = Sirve para localizar los elementos de las filas y Columnas por posicion (i=index / loc=localizacion)
# : = Llama todas las filas 
# :-1 = llama todas las columnas menos la ultima (Purchased)
# values = traigame solo valoes
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 3].values

## Tratamientos de los datos faltantes (nan), remplazamos datos faltantes por la media.
# La libreria sklearn nos ayuda a los tratamiento de los datos, 
# from sklearn = Solo llamamos una fracion de la libreria, con el fin de no llamarla toda.
# missing_values = buscar los valores de toda la columna que tengas NuN
# strategy o estragia saca la medio de los valores
# axis = 0, hace referencia a la columna / axis = 1 hace referencia a las filas

# from sklearn.preprocessing import Imputer
from sklearn.preprocessing import StandardScaler
imputer = StandardScaler(missing_values = "NaN", strategy = "mean", axis = 0)
imputer = imputer.fit(X[:, 1:3])
X[:,1:3] = imputer.transform(X[:, 1:3])