# 💰 Sistema de Legalización de Gastos

Aplicación de escritorio en Python para la gestión y legalización de gastos empresariales.

## 📋 Características

- ✅ Sistema de login con autenticación segura (contraseñas encriptadas)
- ✅ Registro de usuarios
- ✅ Agregar gastos con descripción, monto, categoría y fecha
- ✅ Visualización de gastos en tabla interactiva
- ✅ Estados de gastos: Pendiente, Aprobado, Rechazado
- ✅ Rol de administrador para aprobar/rechazar gastos
- ✅ Persistencia de datos en archivos JSON
- ✅ Interfaz gráfica intuitiva con tkinter

## 🔧 Requisitos

- Python 3.6 o superior
- Tkinter (incluido en la instalación estándar de Python)

## 📦 Instalación

1. Asegúrate de tener Python instalado:
```bash
python --version
```

2. Descarga el archivo `app_gastos.py`

3. Ejecuta la aplicación:
```bash
python app_gastos.py
```

## 🚀 Uso

### Credenciales por defecto
- **Usuario:** admin
- **Contraseña:** admin123

### Funcionalidades

#### Para todos los usuarios:
1. **Registrar nuevo usuario:** Haz clic en "Registrar Usuario" en la pantalla de login
2. **Agregar gastos:** Complete el formulario con:
   - Descripción del gasto
   - Monto en dólares
   - Categoría (Transporte, Alimentación, Hospedaje, Material, Otros)
   - Fecha del gasto
3. **Ver mis gastos:** Todos los gastos aparecen en la tabla del lado derecho

#### Para administradores:
1. **Ver todos los gastos:** Los administradores pueden ver gastos de todos los usuarios
2. **Aprobar gastos:** Selecciona un gasto y haz clic en "✓ Aprobar"
3. **Rechazar gastos:** Selecciona un gasto y haz clic en "✗ Rechazar"

## 📁 Archivos generados

La aplicación genera automáticamente dos archivos JSON:

- `usuarios.json` - Almacena los usuarios y sus credenciales
- `gastos.json` - Almacena todos los gastos registrados

## 🔐 Seguridad

- Las contraseñas se almacenan encriptadas usando SHA-256
- Las contraseñas deben tener mínimo 6 caracteres
- Sistema de roles: usuario normal y administrador

## 📊 Categorías de gastos

- 🚗 Transporte
- 🍽️ Alimentación
- 🏨 Hospedaje
- 📦 Material
- 📌 Otros

## 🎨 Interfaz

La aplicación cuenta con:
- Pantalla de login moderna
- Formulario de registro de usuarios
- Dashboard principal con:
  - Panel para agregar nuevos gastos
  - Tabla con todos los gastos registrados
  - Botones de aprobación (solo para admin)

## 🐛 Solución de problemas

### Error: "No module named 'tkinter'"
En Linux, instala tkinter:
```bash
sudo apt-get install python3-tk
```

En macOS:
```bash
brew install python-tk
```

### La aplicación no inicia
Verifica que estés usando Python 3:
```bash
python3 app_gastos.py
```

## 📝 Notas adicionales

- Los datos se guardan automáticamente después de cada operación
- Los archivos JSON se crean en el mismo directorio que la aplicación
- Se puede personalizar los colores y estilos editando el código
- La aplicación es portable: solo necesitas copiar el archivo .py y los .json

## 🔄 Mejoras futuras sugeridas

- Exportación a Excel/PDF
- Reportes gráficos de gastos
- Adjuntar comprobantes (imágenes)
- Filtros por fecha y categoría
- Base de datos SQLite en lugar de JSON
- Múltiples niveles de aprobación
- Notificaciones por correo

## 📧 Soporte

Si tienes problemas o sugerencias, puedes:
- Revisar el código para personalizarlo
- Agregar nuevas funcionalidades según tus necesidades

---

**Desarrollado con Python 🐍 y Tkinter 🎨**
