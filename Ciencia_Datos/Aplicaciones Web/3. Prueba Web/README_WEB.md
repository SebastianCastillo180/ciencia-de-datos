# 🚗 Sistema Web de Legalización de Gastos para Conductores

Aplicación web desarrollada en Python con Flask para la gestión y legalización de gastos de empresas de transporte y conductores.

## 🎯 Características

### ✅ Funcionalidades Principales
- **Autenticación Segura:** Login con código de conductor y contraseña encriptada
- **Registro de Conductores:** Sistema de registro completo con datos personales y del vehículo
- **Gestión de Gastos:** 
  - Registrar gastos (combustible, peajes, mantenimiento, etc.)
  - Editar gastos pendientes
  - Eliminar gastos no aprobados
  - Filtros avanzados por fecha, tipo y estado
- **Dashboard Interactivo:** Estadísticas en tiempo real
- **Sistema de Aprobación:** Workflow completo para supervisores y administradores
- **Reportes:** Estadísticas por conductor y tipo de gasto
- **Responsive Design:** Funciona en PC, tablet y móvil

### 👥 Roles de Usuario
1. **Conductor:** Puede registrar y gestionar sus propios gastos
2. **Supervisor:** Puede aprobar/rechazar gastos de conductores
3. **Administrador:** Control total del sistema

## 📋 Requisitos del Sistema

### Software Necesario
- Python 3.7 o superior
- SQL Server 2016 o superior
- ODBC Driver 17 for SQL Server
- Navegador web moderno (Chrome, Firefox, Edge)

### Dependencias Python
```bash
pip install flask werkzeug pyodbc
```

## 🚀 Instalación

### Paso 1: Instalar Dependencias

```bash
# Instalar paquetes Python
pip install -r requirements.txt

# En Linux, instalar el driver ODBC
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
```

### Paso 2: Configurar SQL Server

1. **Editar configuración en `app.py`:**
```python
SQL_CONFIG = {
    'server': '192.168.0.22',        # Tu servidor
    'database': 'GastosConductoresDB',
    'username': 'sa',                 # Tu usuario
    'password': 'TuPassword123!',     # Tu contraseña
    'driver': 'ODBC Driver 17 for SQL Server'
}
```

2. **La base de datos se crea automáticamente** al iniciar la aplicación por primera vez

### Paso 3: Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

## 🔐 Credenciales por Defecto

**Usuario:** `ADMIN`  
**Contraseña:** `admin123`

⚠️ **IMPORTANTE:** Cambia estas credenciales en producción

## 📱 Uso de la Aplicación

### Para Conductores:

1. **Registrarse:**
   - Ir a la página de registro
   - Completar datos personales y del vehículo
   - Crear código de conductor único
   - Establecer contraseña (mínimo 6 caracteres)

2. **Iniciar Sesión:**
   - Ingresar código de conductor
   - Ingresar contraseña
   - Click en "Iniciar Sesión"

3. **Registrar Gastos:**
   - Dashboard → Nuevo Gasto
   - Completar formulario:
     - Fecha del gasto
     - Tipo (combustible, peajes, etc.)
     - Descripción detallada
     - Monto
     - Kilometraje (opcional)
     - Ruta (opcional)
     - Número de comprobante (opcional)
   - Guardar

4. **Ver y Gestionar Gastos:**
   - Mis Gastos → Lista completa
   - Filtrar por fecha, tipo o estado
   - Editar gastos pendientes
   - Eliminar gastos no aprobados

### Para Supervisores/Administradores:

1. **Aprobar Gastos:**
   - Administración → Aprobar Gastos
   - Ver lista de gastos pendientes
   - Click en ✓ para aprobar
   - Click en ✗ para rechazar
   - Agregar observaciones (opcional)

2. **Ver Conductores:** (Solo admin)
   - Administración → Conductores
   - Lista completa de conductores registrados
   - Información de contacto y vehículos

3. **Ver Reportes:** (Solo admin)
   - Administración → Reportes
   - Estadísticas por conductor
   - Estadísticas por tipo de gasto
   - Totales y resúmenes

## 📊 Estructura de la Base de Datos

### Tabla: Conductores
- Información personal del conductor
- Credenciales de acceso
- Datos del vehículo
- Rol y permisos

### Tabla: Gastos
- Detalle de cada gasto
- Monto y fecha
- Estado (Pendiente/Aprobado/Rechazado)
- Información de aprobación

### Tabla: Rutas
- Registro de rutas realizadas
- Origen y destino
- Kilometraje
- Horas de trabajo

### Tabla: Vehiculos
- Información de vehículos
- Asignación a conductores
- Estado del vehículo

## 🎨 Estructura del Proyecto

```
proyecto/
├── app.py                    # Aplicación Flask principal
├── requirements.txt          # Dependencias Python
├── README.md                # Esta documentación
├── templates/               # Plantillas HTML
│   ├── base.html           # Template base
│   ├── login.html          # Página de login
│   ├── registro.html       # Registro de conductores
│   ├── dashboard.html      # Dashboard principal
│   ├── gastos.html         # Lista de gastos
│   ├── nuevo_gasto.html    # Formulario nuevo gasto
│   ├── editar_gasto.html   # Editar gasto
│   └── admin_aprobar.html  # Panel de aprobación
└── static/                  # Archivos estáticos
    ├── css/                # Estilos CSS personalizados
    └── js/                 # JavaScript personalizado
```

## 🔧 Configuración Avanzada

### Cambiar Puerto de la Aplicación
```python
# En app.py, línea final:
app.run(debug=True, host='0.0.0.0', port=8080)  # Cambiar 5000 a 8080
```

### Habilitar HTTPS (Producción)
```python
app.run(debug=False, host='0.0.0.0', port=443, 
        ssl_context=('cert.pem', 'key.pem'))
```

### Configurar para Producción
```python
# Cambiar debug a False
app.run(debug=False)

# Usar servidor WSGI como Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 🔒 Seguridad

### Implementado:
✅ Contraseñas encriptadas con Werkzeug (PBKDF2)  
✅ Sesiones seguras con Flask  
✅ Validación de formularios  
✅ Control de acceso basado en roles  
✅ Protección contra SQL Injection (pyodbc parametrizado)

### Recomendaciones Adicionales:
- [ ] Implementar HTTPS en producción
- [ ] Agregar CAPTCHA en login/registro
- [ ] Implementar rate limiting
- [ ] Agregar autenticación de dos factores (2FA)
- [ ] Configurar logs de auditoría
- [ ] Implementar backup automático de BD

## 🐛 Solución de Problemas

### Error: "No se pudo conectar a SQL Server"

**Solución:**
1. Verificar que SQL Server esté corriendo
2. Comprobar credenciales en `SQL_CONFIG`
3. Verificar conectividad de red al servidor
4. Revisar firewall (puerto 1433)
5. Habilitar autenticación SQL Server

### Error: "ModuleNotFoundError: No module named 'flask'"

**Solución:**
```bash
pip install flask werkzeug pyodbc
```

### Error: "No module named 'pyodbc'"

**Solución:**
```bash
pip install pyodbc
# Si falla, instalar driver ODBC primero
```

### La aplicación no carga estilos

**Solución:**
- Verificar conexión a internet (usa Bootstrap desde CDN)
- Revisar consola del navegador (F12)
- Verificar que la carpeta `static/` exista

### No puedo aprobar gastos

**Solución:**
- Solo usuarios con rol 'admin' o 'supervisor' pueden aprobar
- Verificar rol en la base de datos
- Cerrar sesión y volver a iniciar

## 📈 Mejoras Futuras

- [ ] Subir fotos de comprobantes
- [ ] Exportar reportes a Excel/PDF
- [ ] Notificaciones por email
- [ ] App móvil nativa
- [ ] Geolocalización de gastos
- [ ] Integración con sistemas contables
- [ ] Dashboard con gráficos interactivos
- [ ] Chat entre conductor y supervisor
- [ ] Sistema de reembolsos automáticos

## 🆘 Soporte

### Para reportar problemas:
1. Verificar que no sea un error de configuración
2. Revisar logs de la aplicación
3. Consultar la base de datos directamente
4. Revisar permisos de usuario

### Logs de la Aplicación:
```bash
# Ver salida de la consola donde se ejecuta app.py
# Los errores aparecerán en tiempo real
```

### Verificar Estado de SQL Server:
```sql
-- En SQL Server Management Studio
SELECT @@SERVERNAME as Servidor, DB_NAME() as BaseDatos;
SELECT * FROM Conductores;
SELECT * FROM Gastos WHERE estado = 'Pendiente';
```

## 📄 Licencia

Este proyecto es de código abierto y puede ser usado libremente.

## 👨‍💻 Créditos

Desarrollado con:
- **Python 3.x** - Lenguaje de programación
- **Flask 3.x** - Framework web
- **Bootstrap 5** - Framework CSS
- **SQL Server** - Base de datos
- **Bootstrap Icons** - Iconografía

---

## 🚀 Inicio Rápido

```bash
# 1. Clonar/descargar el proyecto
# 2. Instalar dependencias
pip install flask werkzeug pyodbc

# 3. Configurar SQL Server en app.py
# 4. Ejecutar
python app.py

# 5. Abrir navegador
http://localhost:5000

# 6. Login
Usuario: ADMIN
Contraseña: admin123
```

---

**¿Necesitas ayuda?** Revisa la sección de Solución de Problemas o consulta los comentarios en el código fuente.

**¡Sistema listo para producción!** 🎉
