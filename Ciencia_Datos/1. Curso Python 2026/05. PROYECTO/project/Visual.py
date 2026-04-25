
### install openpyxl
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from ydata_profiling import ProfileReport
import openpyxl


st.set_page_config(layout="wide")
st.title("Visualizador de Archivos para Analisis Exploratorio de Datos")

archivo = st.file_uploader("Sube tu archivo CSV o Excel", type=["csv", "xlsx"])

if archivo is not None:
    if archivo.name.endswith(".csv"):
        df = pd.read_csv(archivo)
    else:
        df = pd.read_excel(archivo)

    st.write("Vista previa de los datos:")
    st.dataframe(df.head())

    profile = ProfileReport(df, explorative=True)
    components.html(profile.to_html(), height=1200, scrolling=True)