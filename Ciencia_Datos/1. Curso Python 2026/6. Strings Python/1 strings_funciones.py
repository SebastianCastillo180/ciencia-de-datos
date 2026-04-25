

##Forma 1
# function len
texto="python"
cantidad_caracteres = len(texto) # devuelve el numero de caracteres de la cadena  
print(cantidad_caracteres)  

## Forma 2
texto_hola = len("hola")
print(texto_hola) 


## Forma 3
print(len("vaxidrez"))    


## Forma 4
print(len("")) # devuelve 0 porque no hay caracteres en la cadena vacia
print(len("@?*"))


## print(len(5))  # Esto generará un error porque len() espera un objeto iterable, no un número entero."


print("---"*5) # Imprime una línea de separación con 15 guiones (3 guiones repetidos 5 veces)


# Concatena dos cadenas de texto utilizando el operador +
print("Johan " + "castillo")
print("Johan" + " " + "castillo")
print("Johan " "castillo")