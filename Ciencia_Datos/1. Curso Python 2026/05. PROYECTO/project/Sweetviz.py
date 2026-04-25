### pip install sweetviz openpyxl
### pip install openpyxl
import numpy as np
if not hasattr(np, "VisibleDeprecationWarning"):
    np.VisibleDeprecationWarning = FutureWarning

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import sweetviz as sv
import openpyxl


st.set_page_config(layout="wide")
st.title("Visualizador de Archivos para Analisis Exploratorio de Datos")

archivo = st.file_uploader("Sube tu archivo CSV o Excel", type=["csv", "xlsx"])

if archivo is not None:
    if archivo.name.endswith(".csv"):
        df = pd.read_csv(archivo)
    else:
        df = pd.read_excel(archivo)

    # Convertir columnas object a string para evitar errores de tipos mixtos en Sweetviz
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str)

    st.write("Vista previa de los datos:")
    st.dataframe(df.head())

    report = sv.analyze(df)
    report.show_html("sweetviz_report.html", open_browser=False)

    with open("sweetviz_report.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    components.html(html_content, height=1000, scrolling=True)
