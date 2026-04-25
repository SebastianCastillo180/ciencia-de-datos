# Formulario Rayogas ESP - Puntos Colombia

## 📋 Descripción
Aplicación de escritorio desarrollada en Python con Tkinter para gestionar formularios de clientes del programa Puntos Colombia de Rayogas ESP.

## 🚀 Cómo ejecutar la aplicación

### Opción 1: Doble clic
Simplemente haga doble clic en el archivo `rayogas_formulario.py`

### Opción 2: Desde terminal/cmd
```bash
python rayogas_formulario.py
```

## 🔐 Credenciales de acceso

La aplicación incluye los siguientes usuarios:

| Usuario     | Contraseña   | Rol          |
|-------------|--------------|--------------|
| admin       | rayogas2026  | Administrador|
| usuario     | 12345        | Usuario      |
| operador1   | rayogas123   | Operador     |
| operador2   | rayogas456   | Operador     |
| supervisor  | rayogas789   | Supervisor   |

## 📁 Estructura del proyecto

```
puntos colombia/
├── rayogas_formulario.py  # Aplicación principal
├── README.txt              # Instrucciones en texto plano
├── INSTRUCCIONES.md        # Este archivo
├── rayogas_puntos.db       # Base de datos (se crea automáticamente)
└── uploads/                # Carpeta para archivos adjuntos (se crea automáticamente)
```

## ✨ Características

- ✅ Pantalla de login con autenticación
- ✅ Registro de fecha y hora automático
- ✅ Formulario diferenciado para:
  - Clientes creados (recompra)
  - Clientes nuevos
- ✅ Base de datos SQLite
- ✅ Carga de archivos de cédula
- ✅ Validación de campos
- ✅ Interfaz con colores corporativos (#009fe3)

## 📊 Campos del formulario

### Clientes Creados (Recompra = SI)
- Nombre Completo
- Cédula
- Dirección
- Zona
- Puntos Acumulados

### Clientes Nuevos (Recompra = NO)
- Nombre Completo
- Cédula
- Celular o Número de Contacto
- Ciudad o Municipio
- Zona
- Dirección
- Uso del Gas GLP (Residencial/Industrial/Comercial)
- ¿Inscrito en Puntos Colombia? (SI/NO)
- Monto de la Compra
- Puntos Acumulados
- Autorización de Datos (ACEPTO/NO ACEPTO)
- Foto de Cédula (ambas caras)

## 💾 Base de datos

La aplicación utiliza SQLite y crea automáticamente dos tablas:

### Tabla: `clientes_creados`
- id (autoincremental)
- fecha_registro
- nombre_completo
- cedula
- direccion
- zona
- puntos_acumulados

### Tabla: `clientes_nuevos`
- id (autoincremental)
- fecha_registro
- nombre_completo
- cedula
- celular
- ciudad
- zona
- direccion
- uso_gas
- inscrito_puntos
- monto_compra
- puntos_acumulados
- autorizacion_datos
- archivo_cedula

## 📝 Notas importantes

1. **Python requerido**: Se necesita Python 3.7 o superior instalado
2. **Tkinter**: Viene incluido con Python, no requiere instalación adicional
3. **Archivos adjuntos**: Se guardan en la carpeta `uploads/` con formato: `{cedula}_{timestamp}.{extension}`
4. **Base de datos**: Se crea automáticamente la primera vez que ejecuta la aplicación

## 🛠️ Requisitos técnicos

- Python 3.7+
- Tkinter (incluido con Python)
- SQLite3 (incluido con Python)
- **Pillow (Opcional)**: Para mejor calidad del logo

### Instalación de dependencias opcionales

Para mejor visualización del logo, instalar Pillow:

```bash
pip install -r requirements.txt
```

La aplicación funciona sin Pillow, pero con menor calidad de imagen.

## 📞 Soporte

Para preguntas o problemas, contacte al administrador del sistema.

---

**Desarrollado en Python con Tkinter**
© 2026 Rayogas ESP
