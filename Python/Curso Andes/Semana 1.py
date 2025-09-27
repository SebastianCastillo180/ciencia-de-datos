# -*- coding: utf-8 -*-
"""
Fecha 7 21:40:06 2024

Comando de Ejecución F5 ejecutamos todo nuestro codigo y con paramos
en alguna casilla y ejecutamos F9 para ejecutarla.

Los signos + funsionan como concatenacion.
Las "" Sirver para guardar un texto para ejecutar
Los () Sirver para guardar valores para ejecutar
"""


print("10 pulgadas son "+str(10*2.54)+" centimetros")
print("10 pies son", (10*30.48),"centimetros y", (10*0.3048), "metros")
"""
Semana #1

¡Te damos la bienvenida al módulo 1! En este módulo presentaremos en detalle los conceptos básicos de cualquier lenguaje de programación y los explicamos e ilustramos usando el lenguaje de programación Python. Los conceptos principales que estudiaremos en este módulo son los siguientes: tipos de datos, variables, expresiones, operadores, definición e invocación de funciones y parámetros. Ten en cuenta que el tiempo estimado para la realización de todas las actividades de este módulo es de cerca de 12 horas, tiempo que puedes usar de acuerdo con tus posibilidades. Nuestra recomendación es que desarrolles todas las actividades en el orden propuesto y que consideres hacerlo en un tiempo de dos semanas.
Objetivos de aprendizaje.
- Resolver problemas bien definidos utilizando un algoritmo
- Entender los diferentes tipos de datos, la creación de variables y operaciones básicas del lenguaje
- Comprender funciones básicas de Python y cómo se llaman/invocan
- Llamar funciones con parámetros y funciones desde otras funciones (composición de funciones)
- Implementar funciones propias, entendiendo el concepto de variables locales y parámetros
- Manejar la entrada y salida de información en un programa
- Construir interfaces de consola
- Crear módulos para agrupar funciones relacionadas, y usar dichos módulos en sus programas
- Utilizar elementos que hagan el código mucho más comprensible y fácil de mantener
- Explorar los ambientes básicos de trabajo en Python (Spyder)

"""

"""
Lección 1 - Valores y tipos de datos

1. Literal - es un valor espesifico
Ejemplo 1: "Hola mundo"
Ejemplo 2: 10

2. Expresion - Es la convinacion de valores y operadores para generar una resultado
Ejemplo 1: 7 + 3


3. Los valores o tipos de datos estan clasificados en:
    
3.1 10 es un entero = Int
Ocupan menos memoria que los float y las operaciones son
mas rapidas

3.2 4.5 es un decimal = float

3.3 "Hola Mundo!" es una cadena de caracter = str
Cadenas o secuencias de caracteres: letras, números, espacios, 
signos de puntuación, emoticones, etc.

4 Tipos de Datos Type
Para conocer el tipo de un valor Python tiene una función
llamada type

Ejemplo 1: type (3.2)
           float
Ejemplo 2: type (17)
           int
Ejemplo 3: type ("Hola mundo!")
           str           
Ejemplo 4: type ("3.2")
           str
Ejemplo 5: type ('3.2')
           str           
"""


"""
Lección 2 - Variables e instrucción de asingación
Las variables se usan para guardar valores que se necesitaraán más 
adelante en el programa

Ejemplo 1:
    pi = 3.14159265359    (Se gaurdo pi con la varible 3.14159265359)
    r  = 1.298373
    perimetro = 8157918156839218
    Área = 5.296010335524904
    
Importante
Nombre de la variable y palabras reservadas
- Debe tener letras minusculas, mayusculas, digitos. 
- El primer caracter no puede ser un digito.
- Python distingue entre mayusculas y minusculas.
- No puede coincidir con una palabra reservada. 
and, as, assert, break, class, continue, def, del,
elif, else, except, exec, finally, for, from, global,
if, import, in, is, lambda, try, while, with, 
yield, True, False, Nome

"""

pi = 3.14159265359
r  = 1.298373
perimetro = 8157918156839218
Área = 5.296010335524904
2 * pi * r  ### Resultado 1
pi * r ** 2 ### Resultado 2 




"""
Lección 3 - Expresiones, operadores aritmeticos y operaciones
sobre strings.
- Una expresion es una combinacion de valores, variable y
operadores.
- La evaluacion de una expresion produce un valor. Por esto las 
expresiones pueden aparecer al lado derecho de una asignacion:
    
               Variable = Valor o Expresion

Ejemplo 1
x = 3 + 7
x

- Los operadores son simbolos que representan calculos.

Operacion         Operador     Aridad     Precedencia   
--------------    --------    --------    -----------
Exponenciacion       **        Binario         1
--------------    --------    --------    -----------
Identidad            +         Unario          2
Cambio de Signo      -         Unario          2
--------------    --------    --------    -----------
Multiplicacion       *         Binario         3
Division             /         Binario         3
Division Entera      //        Binario         3
Modulo (o resto)     %         Binario         3
--------------    --------    --------    -----------
Suma                 +         Binario         4
Resta                -         Binario         4


"""



"""
Lección 4 - Expresiones, operadores aritmeticos y operaciones
sobre strings.
- Una expresion es una combinacion de valores, variable y
operadores.
- La evaluacion de una expresion produce un valor. Por esto las 
expresiones pueden aparecer al lado derecho de una asignacion:
    
               Variable = Valor o Expresion

Ejemplo 1
x = 3 + 7
x

- Los operadores son simbolos que representan calculos.

Operacion         Operador     Aridad     Precedencia   
--------------    --------    --------    -----------
Exponenciacion       **        Binario         1
--------------    --------    --------    -----------
Identidad            +         Unario          2
Cambio de Signo      -         Unario          2
--------------    --------    --------    -----------
Multiplicacion       *         Binario         3
Division             /         Binario         3
Division Entera      //        Binario         3
Modulo (o resto)     %         Binario         3
--------------    --------    --------    -----------
Suma                 +         Binario         4
Resta                -         Binario         4


- Conversion de tipos
Se usan 3 funsiones (int, float, str)

Ejercicio int (entero)
Si recibe un numero decimal devuelve el entero

int(2.1)      Rta:  2
int(-2.9)     Rta: -2
int("2")      Rta: "2"
int(-)        Rta:  3
int("Hola")   Rta: Error


Ejercicio float (decimal)
Si recibe un numero entero devuelve el numero.

float(3)       Rta: 3.0
float("4.5")   Rta: "4.5"
float(4.5)     Rta: 4.5


Ejercicio str (string)
-Recibe un numero y devuelve un representacion de este string
- Si recibe una cadena de caracteres devuelve el mismo valor

str(2.1)             Rta: 2.1
str(34+27)           Rta: '61'
str(104.5 + 34.76)   Rta: '139.26'   
cadena = "El año de nacimiento es: " + str(1924)
cadena

cadena2 = "Su silla asignada en el vuelo es :" + str(21) + "C que corresponde a pasillo"
"""



"""
Lección 5 - Funciones
- Una funsion empaqueta y serapa un conjunto de instruciones que ejecutan una tarea especifica
- Principal funsion Organiza en segmento
- Le podemos dar cualquier nombre, menos las reservadas.


Leccion 5.1 Funciones de python
python dispone de una serie de funciones integradas al lenguaje, que pueden
ser utilizadas para crear nuestros propios programas.

- Funciones a utilizar: (int, float, str, type)

- Otras funciones utiles
  abs()   - Valor absoluto 
  round() - redondeo
  
ejemplo abs
abs(-3)      Rta: 3
abs(3)       Rta: 3
abs(0)       Rta: 0
abs 0        Rta: Error

ejemplo round
round(2.1)   Rta:  2
round(2.9)   Rta:  3
round(-2.9)   Rta: -3
round(2)   Rta: 2

- Funciones utiles sobre cadenas
ort()
devuelve el valor numerico que corresponde a un caracter 
en la tabla ASCll
Ejemplo ort
ord('a')     Rta: 97
ord('A')     Rta: 65

chr()
el contrario de ord
Ejemplo chr
chr('97')     Rta: 'a'
chr(65)       Rta: 'A'
chr(225)      Rta: 'á'


- Funciones input, print
Para leer datos tecleados por el usuario. Devuelve un string
Ejemplo imput
n = imput("Por favor ingrese nombre: ") 

Ejemplo print
print("El volumen de la esfera es : ", 4/3 * 3.1416 * radio ** 3) 
print("El volumen de la esfera es : ", 4/3 * 3.1416 * float(input("Cual radio es ?")) ** 3) 

- Funciones help
Para saber cuales son parametros de una funcion predefinida 
en python se puede usar la funcion help()


---------------------------------------------------------
Problemas # 1 
x1 = int(input("ingrese el valor de x1: "))
x2 = int(input("ingrese el valor de x2: "))
x3 = int(input("ingrese el valor de x3: "))

### Rotacion de los valores

temporal = x1
x1 = x3
x3 = x2
x2 = temporal

print(str(x1)+", "+str(x2)+", "+str(x3))


---------------------------------------------------------
Problemas # 2
Calcular el valor futuro del monto inicial 

capital = float(input("Ingrese el capital inicial: "))
tasa = float(input("ingrese tasa anual: "))
tiempo = int(input("ingrese el numero de años: "))

valor_futuro = capital * (1+(tasa/100))**tiempo

print("el valor futuro del monto inicial es de $" +str(valor_futuro)+", transcurrido"+str(tiempo)+" años y a una tasa del" +str(tasa)+"% anual") 
---------------------------------------------------------


- Funciones Nuevas (invocar o llamar)
Ademas de las funiones de python, que vimos, podemos 
definir nuestras propias funciones!

   - Es una forma de extender el lenguaje y de enseñar 
   a python hacer calculos que inicialmente no sabe hacer

La sintaxis para definir nuestras propias funciones es:
    
    
Ejemplo 1
def nombre(parametros):
          instruciones
          

Ejemplo 2 
abs(-3)             - 1 Parametro  
Rta: 2

abs(round(2.45,1))  - 2 Parametro
Rta: 2.5 


Ejemplo 3
def cuadrado(x: float)->float:
## calcula el cuadrado de un numer dado
    return x ** 2

## Programa principal
print(cuadrado(2))
a= 1 + cuadrado(3)
print(cuadrado(a+3))


---------------------------------------------------------
---------------------------------------------------------
Importante
- Funciones diferentes son independientes:
Ejemplo 1:
    
    def cuadrado(x: float)->float:
        return x ** 2
    
    def cubo(x: float)->float:
        return x * x * x
    
    print(cuadrado(2))
    print(cubo(3))
    
Las dos funciones reciben un parametros cada una Pueden 
tener el mismo nombre, son parametros DIFERENTES porque 
estan en funciones diferentes.


- Parametros es diferente a argumento
Ejemplo 1:   
     def cubo(x: float)->float:
         return x * x * x
     
     y = 2 
     print(cubo(y))
     
y - Es una variable que se usa para guardar el valor 2.
---------------------------------------------------------
---------------------------------------------------------

- Definicion de funciones con varios parametros

Ejemplo 1:
    
    def area_rectangulo(altura: float, anchura, float)->float:
        return altura * anchura
    
    
Ejemplo 2:
    
    def area_rectangulo_2(altura: float, anchura, float)->float:
        area = altura * anchura
        return area
    
Ejemplo 3:
Traer informacion del teclado
     
    def cubo()->int:
        x = int(input("Teclee el valor:"))
        return x * x * x
    
    print("El resultado es:", str(cubo))
    
    
    

- Variables Locales

En el cuerpo de las funciones es posible definir 
y usar variables.

Se diferencian de las variables que definimos fuera
de cualquier funcion, es decir en lo que llamamos
el programa principal.

Ejemplo
def volumen_cilindro(radio_base = float, altura = float)->float:
    area_base = 3.1416 * radio_base * radio_base
    return area_base * altura

r = float(input("Digite el radio :"))
a = float(input("Digite la altura :"))
print("El valor es ", str(volumen_cilindro(r, a)))


Ejemplo 2 
def inclementar(a: int)-> int:
    a = a + 1
    return a

a = 1 
b = inclementar(a)
print("Valor de a :", a)
print("Valor de b :", b)

---------------------------------------------------------
Ejemplo 2
def calcular_area_cuadrado(lado: float)-> float:
    return lado * lado


def calcular_area_circulo(radio: float)-> float:
    return 3.1416 * radio * radio

def calcular_diferencia(lado: float)-> float:
    return calcular_area_cuadrado(lado) - calcular_area_circulo(lado/2)


### Programa Principal
lado_cuadrado = float(input("Digite el lado del cuadrado:"))
print("El area de las esquinas es: ", round(calcular_diferencia(lado_cuadrado),2))
---------------------------------------------------------

-------------------------------------------------------------
-------------------------------------------------------------
Ejercicio de definicion de funciones

-- Primer Punto
Defina una funcion que convierta grados fahreneit en grados
centigrados. para calcular los grados centigrados debe restar 32 
a los grados fahreneit y multiplicar el resultado por cinco novedos

def fahrenheit_a_centigrados(grados_f: float)->float:
    grados_cent = (grados_f -2)*(5/9)
    return grados_cent

-- Segundo Punto
Defina una funcion que convierta gradps centigrados en grados fahreneit


-- Tercero punto
Defina una funcion que convierta radianes en grados. recuerde
que 360 grados son 2pi radianes

-- Cuarto punto
Se define una función que convierta radianes en grados. Recuerde que
360 grados son 2pi radianes.
## Nota: Se ejecuta en la terminal
def radianaes_a_grados(radianes:float)->float:
    pi = 3.14159
    return (360*radianes)/(2*pi)

-- Quinto punto
Defina una función que convierta grados en radianes
def radianaes_a_grados(grados:float)->float:
    pi  = 3.14159
    rad = (2*pi*grados)/360
    return rad


-- Sexto punto
Defina una función que reciba un número entero positivo de 4
cifras (digitos y devuelva el número invertido)

Ejemplo 1
def invertir_numero(numero:int)->int:
    unidades  = numero % 10
    numero  //= 10
    decenas   = numero % 10
    numero  //= 10
    centenas  = numero % 10
    numero  //= 10
    millares  = numero % 10  
    
    inverso = (unidades*1000)+(decenas*100)+(centenas*10)+millares
    
    return inverso

Ejemplo 2

def invertir_numero(numero:int)->int:
    unidades  = numero % 10
    numero  //= 10
    decenas   = numero % 10
    numero  //= 10
    centenas  = numero % 10
    numero  //= 10
    millares  = numero % 10  
    
    inverso = str(unidades) + str(decenas) + str(centenas) + str(millares)
    
    return inverso




-------------------------------------------------------------
-------------------------------------------------------------
https://www.lawebdelprogramador.com/foros/Python/1800067-programa-en-phyton-cambio-a-retornar.html

Ejercicio: 
Considere el software que se ejecuta en una máquina expendedora. 
Una de las tareas que debe realizar es determinar cuánto cambio 
debe entregarle al cliente luego de que paga. Escriba una función 
que recibe la cantidad de dinero (en pesos) a dar como cambio al 
cliente y retorne un mensaje con la cantidad de monedas de cada 
denominación que deben ser entregadas, teniendo en cuenta que el 
cambio se debe otorgar con la menor cantidad de monedas posible.
La máquina cuenta con monedas de 500, 200, 100 y 50 pesos, y el
 cambio total se entregará con monedas de estas denominaciones. 
 El mensaje retornado DEBE seguir el siguiente formato: “A,B,C,D” 
 (sin espacios intermedios) donde A, B, C y D son la cantidad de 
 monedas de 500, 200, 100 y 50, respectivamente.
Su solución debe tener una función de acuerdo con la siguiente 
especificación:
    
    
Nombre de la función: calcular_cambio

Si lo requiere, puede agregar funciones adicionales.

Solucion
def calcular_cambio(cambio:int)->int:
    A  =    cambio // 500
    B  =   (cambio % 500) // 200
    C  =  ((cambio % 500) % 200) // 100
    D  = (((cambio % 500) % 200) % 100)// 50
    
    cadena = str(A) + "," + str(B) + "," + str(C) + "," + str(D)
    
    return cadena
    
-------------------------------------------------------------
-------------------------------------------------------------
-------------------------------------------------------------
-------------------------------------------------------------
Una agencia de viajes necesita informar a sus clientes la hora de llegada 
de sus vuelos. Se conoce la hora de partida del vuelo (en horas, minutos y 
segundos) y la duración del vuelo (en horas, minutos y segundos).
Cree una función que retorne la hora de llegada del vuelo en una 
cadena con el formato “HH:mm:ss” donde HH es la hora, mm los minutos 
y ss los segundos de la hora de llegada del vuelo. 
La hora está dada en formato de 24 horas. Si alguno de los 3 números 
de la respuesta es menor a 10, sólo se necesita un dígito 
('7' en lugar de '07').


https://www.coursera.org/learn/programacion-python/supplement/bpuzc/reto-4-hora-de-llegada-de-vuelo

def calcular_horario_llegada(hora_salida:int,minuto_salida:int,segundo_salida:int,duracion_horas:int,duracion_minutos:int,duracion_segundos:int)->int:
    hora_llegada = ((segundo_salida + duracion_segundos)// 60) + ((minuto_salida + duracion_minutos)// 60) + (hora_salida + duracion_horas)
    minuto_llegada = ((segundo_salida + duracion_segundos)// 60) + ((minuto_salida + duracion_minutos)%60)
    segundo_llegada = (segundo_salida + duracion_segundos) % 60
    if segundo_llegada > 59:
        minuto_llegada = minuto_llegada + 1
    if minuto_llegada > 59:
        hora_llegada = hora_llegada + 1
    if hora_llegada == 0 or hora_llegada > 23:
        hora_llegada = hora_llegada - 24
    return str(hora_llegada) + ":" + str(minuto_llegada) + ":" + str(segundo_llegada)
-------------------------------------------------------------
-------------------------------------------------------------


Lección 6 - Estilo de Programación

## 6.1 Estilo
Hay muchas formas en las que se puede escribir el mismoprograma

- Incluir comentarios adicionales 
- Cambiar nombres de las variables y de las funciones
- Cambiar la descomposición en funciones.


## 6.2 Responsabilidades
El código que esbribamos hoy posiblemente nos va aompañar por muchos tiempos.

## 6.3 Aspectos 
# Nombramiento de variables y funciones

- Utilice nombres claros, qué es lo que van a guardar la variable.
- Evite nombres muy cortos (ambiguedad)
- Para las funciones utilice nombres que indiquen lo qué hace la función
(calcular_area_tirangulo ó area_triangulo)

# 6.3.1 Para los nombres utiliza estándares

- Uso de mayúsculas, minúsculas y nombres compuesto.

#  6.3.1 En Python 
- El carácter _ para separar las palabras
- Los identificadores se esbriben en minuscula
- Alfabeto ingles para evitar problemas de codificación


## 6.4 Documnetacion de funciones
Formato consistente que incluya:
    - Descripción:  Objetivo de la función
    - Parametros:   nombre y tipo de cada uno con una breve descripciión
    - Retorno:      descripcion de lo que retorna la funcion y su tipo
    
Ejemplo 6.4
def calcular_IMC(peso: float, altura: float)->:
    --- Calcula el indice de masa corporal de una persona a partir de la 
        información recibida.
    Parametros:
        peso (float) peso de la persona, en kilogramos.
        altura (float) altura de la persona, en metros.
    Retorna:
        float: El índice de masa corporal de la persona en kg/m^2
    

Lección 7 - Construcion e iportancia de modulos

- Un modulo es una coleccion de finciones y de valore s que se enentran 
en un archivo.
- Es posible utilizar un módulo en varios programas. Esto nos permite ahorrar 
el tiempo que requeriria escribir una misma funcion que se necesite en 
diferentes programas.
- Se recimienda que las funciones se agruoen en modulos segun su ambito 
de aplicacion.

Ejmeplo - Modulo de conversacion dolares pesos
----------------------------------------------

En este ejemplo tenemos dos modulos:
    1. El primero agrupa funciones que nos ayuda a resolver el problema
    (es decir la logica del programa)
    2. El segundo modulo se encarga de interactuar con el usuario pidiendo
    la informacion necesaria. Note que la TRM, se pide una sola vez desde la funcion 
    iniciar_aplicacion(), mientras que las cantidades se piden desde las funciones
    ejecutar_
    
    
Ejecicio 


def convertir_a_dolares(pesos: float, trm: float)-> float:
    return pesos / trm

def convertir_a_pesos(dolares: float, trm: float)-> float:
    return dolares / trm

import libreria as lb
def ejecutar_convertir_a_dolares(trm: float)->None:
    pesos = float(input("Ingrese la cantidad de pesos: "))
    dolares = lb.convertir_a_dolares(pesos, trm)
    print(pesos, "pesos son", round(dolares,2) , "dolares")
    
def ejecutar_convertir_a_pesos(trm: float)->None:
    dolares = float(input("Ingrese la cantidad de dolares: "))
    pesos = lb.convertir_a_pesos(dolares, trm)
    print(dolares, "dolares son", round(pesos,2) , "pesos")
    
def iniciar_aplicacion ()->None:
    trm = float(input("Ingrese la TRM: "))
    ejecutar_convertir_a_dolares(trm)
    ejecutar_convertir_a_pesos(trm)
    
iniciar_aplicacion()


 Lo primero es importar el módulo, para esto, al inicio del programa 
 usamos la palabra reservada "import", le damos el nombre del módulo 
 que queremos importar y le asignamos un alias dentro del módulo después
 de la palabra reservada "as". 
 Como es probable que tengamos que usar 
 constantemente este alias, mi recomendación es que usen nombres cortos.
 Y cuando ya vayamos a embocar una función, entonces a través del alias y
 el operador punto, podemos hacerlo como lo vemos en las líneas cinco y diez. 
 Y de esta manera, usando módulos, podemos estructurar nuestros programas.
 Y aunque este tema es corto, es muy útil y lo utilizaremos constantemente.
 Cerremos entonces con una pregunta.
    

Lección 8 - Modulo Final contexto

- Seguro
- Tener buen desempeño 
- Facil de usar (usabilidad)
Este ultimo, esta directamente relacionado con la interfaz
de usuario.

- Escalable
- Tolerante a fallos
- Pero lo mas importante es que tan facil es hacer
un cambio o en otras que tan mantenible.


## 8.1 Interfaz de usuario

- La interfaz de usuario es el medio a traves del cual el 
usuario puede comunicarse con un programa.
- Existen varios tipos, pero en este curso nos centraremos 
unicamente en las interfaces basadas basadas en consola.

- 8..2 Sepración entre interfaz de usuario y logica del programa

Para que un programa sea facil de entender, mantener y extender
es recomendable que su logica sea independiente de la interfaz
# La interfaz se encarga de la comunicacion con el usuario (Enrada
y salida de datos) y se implementa en una archivo seprado que
contiene el programa principal
# La logica se encuentra implementada en funciones que 
componen modulos, los cuales se usan o llaman desde la interfaz


-------------------------------------------------------------
-------------------------------------------------------------
Manos a la obra
Queremos crear un programa que realice el cambio de las divisas
de dolares a pesos y viceversa.

COP = USD
USD = COP

Necesitamos entonces el monto de dinero a convertir, y la tasa
representativa del mercado (TRM)

def convertir_a_dolares(pesos:float, trm:float)->float:
    return pesos/trm

def convertir_a_pesos(dolares:float, trm:float)->float:
    return dolares*trm


Entradas
TRM
Cantidad de USD o COP

Salida
ConversiÓn a USD O COP

import libreria as lb

def ejecutar_convertir_a_dolares(trm:float)->float:
    pesos = float(input("Ingrese la cantidad de pesos: "))
    dolares = lb.convertir_a_dolares(pesos, trm)
    print(pesos, "pesos son", round(dolares,2),"dolares")
    
    
def ejecutar_convertir_a_pesos(trm:float)->None:
    dolares = float(input("Ingrese la cantidad de pesos: "))
    pesos = lb.convertir_a_pesos(dolares, trm)
    print(pesos, "dolares son", round(pesos,2),"pesos")
    
def iniciar_aplicacion()->None:
    trm = float(input("Ingrese la TRM: "))
    ejecutar_convertir_a_dolares(trm)
    ejecutar_convertir_a_pesos(trm)
    
iniciar_aplicacion()
-------------------------------------------------------------
-------------------------------------------------------------


"""





















































""" Considera el siguiente fragmento de código: 
1. Una vez se hayan ejecutado todas las instrucciones,¿qué valor tendrá la variable_1?
Rta. '8.0'

variable_1 = "4"
variable_2 = int(str(variable_1))
variable_3 = variable_1*2
variable_1 = variable_2*2
variable_2 = variable_1
variable_1 = str(float(variable_2))
variable_1

2. Una vez se hayan ejecutado todas las instrucciones,¿qué valor tendrá la variable_3?
Rta: 2468
variable_1 = 1234
variable_2 = str(variable_1)
variable_3 = float(variable_1)
variable_1 = float(variable_1)
variable_2 = int(variable_1)
variable_3 = int(float(variable_1) + float(variable_2))
variable_3


3. Seleccione la única afirmación correcta que explique la línea en la que se encuentra el error, su naturaleza y cómo solucionarlo.
Rta: 3
def funcion_1()->str:
    return "Hola mi amigo " 

def funcion_2(palabra:str)->str:
    return funcion_1()+str(palabra)

resultado = print(funcion_2("Juan"))
print("El resultado de mi funcion es: " + resultado)


def funcion_1()->str:
    return "Hola mi amigo " 

def funcion_2(palabra:str)->str:
    return funcion_1()+str(palabra)

resultado = print(funcion_2("Juan"))
print("El resultado de mi funcion es: " + resultado)




6. Estudia con cuidado el siguiente programa. Asume que el usuario ingresa 56Kg y 1.62mt como valores de peso y estatura respectivamente. 

def calcular_IMC( peso: float, altura: float)->float:
                 
    imc = peso/((altura)**2)
    return imc

peso = input("Digite su peso en kilogramos: ")
estatura = input("Digite su estatura en metros: ")
indice = calcular_IMC(float(peso), float(estatura))
print("Su indice de masa corporal es: ", indice)


9. Calcula caida de un objeto

altura = float(input("Ingrese la altura: "))
velocidad = float(input("Ingrese la velocidad: "))
 
vel_en_caida_libre = round(altura/velocidad,2)
 
print("El tiempo en llegar al suelo: {}".format(vel_en_caida_libre))


10. Calculo edad

import datetime

# Introduce la fecha de nacimiento en formato 'YYYY-MM-DD'
fecha_nacimiento = input("Introduce tu fecha de nacimiento (YYYY-MM-DD): ")
# Calcula la edad a partir de la fecha de nacimiento
fecha_nacimiento = datetime.datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
edad = datetime.datetime.now().year - fecha_nacimiento.year
# Imprime la edad calculada

print("Tu edad es:", edad)

"""





