# 1. Ingresar la cantidad en dolares
# 2. Realizar la formula matematica convertir a euros
# 3. Imprimir el resultqado en la consola, se debe realizar con un boton

import streamlit as st

# 1. Titulo de la aplicacion
st.title("Conversor de Dolares a Euros")

# 2. Ingresar la cantidad en dolares
dolares=st.number_input("ingrese la cantidad de dolares")
5
# 3. Convierte en valor el euros
euros=dolares*2
euros=str(euros) # Convierte a texto

# 4. Cuando le de click al boton, se debe imprimir el resultado
st.button("Procesar", on_click=print("Aqui se imprimira el resultado: " + euros))