# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 18:15:33 2024

@author: analistabi
"""

"""
Semana #2

Te damos la bienvenida al módulo 2! En este módulo presentaremos los conceptos necesarios para que un programa no siempre se ejecute de la misma manera, sino que pueda tomar decisiones dependiendo de las condiciones en que se ejecute y de los datos que proporcione el usuario. En este módulo también introducimos una estructura de datos (diccionarios) que permite manejar información más compleja que la que permiten los tipos simples presentados hasta el momento. Los conceptos principales que estudiaremos en este nivel son los siguientes: valores de verdad (booleanos), instrucciones condicionales, diccionarios y paso de parámetros por valor y por referencia. Ten en cuenta que el tiempo estimado para la realización de todas las actividades de este módulo es de cerca de 13 horas, tiempo que puedes usar de acuerdo con tus posibilidades. Nuestra recomendación es que desarrolles todas las actividades en el orden propuesto y que consideres hacerlo en un tiempo de dos semanas.
Objetivos de aprendizaje
Entender los conceptos de tablas de verdad y álgebra booleana
Utilizar expresiones y operadores relacionales, así como expresiones y operadores lógicos
Comprender el tipo de dato booleano
Utilizar instrucciones condicionales (if-else, en cascada y anidados) dentro de sus programas para la solución de problemas por casos
Utilizar nuevas operaciones sobre strings
Manipular diccionarios
Utilizar diccionarios para manejar elementos que tienen las mismas características
Aplicar el concepto de "dividir y conquistar" al solucionar problemas

"""


"""
Lección #1

##### 1. Booleanos y sus operaciones
Booleanos =  son un tipo de dato que representan valores lógicos y que pueden tener dos valores: True (verdadero) o False (falso). 

- Un dato de tipo logico solo puede presentar uno de dos valores True o False

- Com ocon los demas tipos de datos que hemos visto (int, float o string), pueden existir expresiones, variables y 
funciones con valores booleanos(bool) 

operaciones booleana basicas:
    
    -----Operador---   --Se lee como-- 
    and (conjuncion)         y
    or  (disyuncion)         o
    not (negacion)           no

##### 2. Tablas de verdad & Algebla Booleana
Algebra Booleana = Se llama algebra a un conjunto de reglas que usan para simplificar expresiones. Por ejemplo, 
                   gracias al algebra elemental sabemos que:  n * O == 0
########################################
Conjunto (and)
True   True  = True
True   False = False
False  True  = False
False  False = False

Disyuncion (or)
True   True  = True
True   False = True
False  True  = True
False  False = False

Negacion (Not)
a     Not a
True  False
Flase True
########################################
     
Ejercicio:
  a = 45
  b = 30
  c = 10

    a+c >= b                        ## = True
    b-c < a-b                       ## = False
    (a>b and b>c) or (b<c and a>b)  ## = True
    a*b < a*b/c                     ## = False
    a>c and b                       ## = 30
"""          




"""            

Lección #2


##### 2. Instruciones condicionales

## Instruciones condicionales
Estan instruciones son llamadas (bloques). No hay 
limites en la cantidad de intruciones que componene un 
bloque, pero debe haber al menos una instruccion en cada uno.

ejemplo:
    if EXPRESION BOOLEANA:
        INTRUCIONES_1       ### se ejecutan si al evaluar la condicion da True
    
    else:
        INTRUCIONES_1       ### se ejecutan si al evaluar la condicion da False     
                       
ejemplo 2:
    
import math

x = int(input("Digite un numero: "))

if x < 0:
    print("El numero negativo ", x, "no es valido aqui")
    y = x
    x = 42
    print("Decidi usar el numero 42 en lugar de ", y)

print("La raiz cuadrada de: ", x, "es", math.sqrt(x))   



ejemplo 3 condicion cascada ##############

def funcion_a()->None:
    print ("Usted escogio la opcion a del menu")
    
def funcion_b()->None:
    print ("Usted escogio la opcion b del menu")
    
def funcion_c()->None:
    print ("Usted escogio la opcion c del menu")
    
def funcion_d()->None:
    print ("Usted escogio la opcion c del menu")
    
print("Menu principal")
print("Opcion a")
print("Opcion b")
print("Opcion c")
print("Opcion d")

x = input("Seleccione su opcion: ")

if x == "a":
   funcion_a()
elif x == "b":
   funcion_b()
elif x == "c":
   funcion_c()
elif x == "d":
   funcion_d()
   
else:
    print("Seleccion invalida")
    
ejemplo 4 condicion consecutivas ##############

num1 = int(input("Digite un numero:"))
num2 = int(input("Digite el segundo numero:"))
num3 = int(input("Digite el tercer numero:"))

cuantos = 0
if (num1 % 2 == 0):
    cuantos += 1
if (num2 % 2 == 0):
    cuantos += 1
if (num3 % 2 == 0):
    cuantos += 1
    
print("De los tres numeros digitados hay", cuantos, "pares")


ejemplo 5 Instruciones condicionales anidadas ##############

## Manos a la obra #############################
Escriba una funcion que reciba por parametro un numero entero y devuelva

def rango_numero(x: int)->int:
    if x < 0:
        respuesta -1
    elif x < 1000:
        respuesta 0
    elif x <= 10000:
        respuesta 1
    else:
        respuesta 2
    
    return respuesta







"""