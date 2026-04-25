
##################################################################
# Ejericio 1: Función que retorna un valor
def sumar(a,b):
    c = a + b
    return c  #### Termina la función y devuelve el valor de c

resultado = sumar(89,56)
print(resultado)


##################################################################
# Ejericio 1: Función que retorna un valor pero también imprime el resultado
def sumar(a,b):
    c = a + b
    print("El resultado de la suma es:", c)  #### Imprime el resultado pero no lo devuelve
    return c  #### Termina la función y devuelve el valor de c

resultado = sumar(89,56)
print(resultado)

