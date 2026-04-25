import streamlit as st
import pandas as pd

def calcular_subtotal(nombre_producto, precio_producto, cantidad_producto):  # Función para calcular el subtotal
    subtotal = float(precio_producto) * float(cantidad_producto)             # Calcular el subtotal multiplicando el precio por la cantidad
    nueva_fila = {
        "producto": nombre_producto, 
        "precio": precio_producto, 
        "cantidad": cantidad_producto, 
        "subtotal": subtotal}          
    st.session_state.table_data = pd.concat(
               [st.session_state.table_data,
               pd.DataFrame([nueva_fila])],
               ignore_index=True
            )                                                                  # Crear un diccionario con los datos del producto


if "table_data" not in st.session_state:                                       # Verificar si 'table_data' no está en el estado de sesión
    st.session_state.table_data = pd.DataFrame(                                # Crear un DataFrame vacío con las columnas especificadas
                    columns=["producto","precio","cantidad", "subtotal"]
                    )


st.title("Supermercado el Buen Vivir")                                              # Título de la aplicación


with st.form("producto_form"):                                                      # Crear un formulario con el identificador 'product_form'
    producto_nombre = st.text_input("Ingrese el Nombre del Producto")               # Campo de entrada para el nombre del producto
    precio_producto = st.number_input("Ingrese el Precio del Producto")             # Campo de entrada para el precio del producto
    cantidad_producto = st.number_input("Ingrese la Cantidad del Producto")         # Campo de entrada para la cantidad del producto
    
    subtotal_boton = st.form_submit_button("Comprar Producto")                      # Botón para enviar el formulario

if subtotal_boton:                                                                  # Verificar si se ha presionado el botón de enviar
    calcular_subtotal(producto_nombre, precio_producto, cantidad_producto)   


st.dataframe(st.session_state.table_data)                                            # Mostrar el DataFrame con los datos de los productos comprados   


if st.button("Calcular Total"):                                                        # Botón para calcular el total de la compra
    total = (st.session_state.table_data["precio"] *
        st.session_state.table_data["cantidad"]).sum()     # Calcular el total multiplicando el precio por la cantidad para cada producto
    

    st.subheader("Total a Pagar")
    st.write("El precio total es:"  +str(total))                                         # Mostrar el total a pagar con formato de moneda


