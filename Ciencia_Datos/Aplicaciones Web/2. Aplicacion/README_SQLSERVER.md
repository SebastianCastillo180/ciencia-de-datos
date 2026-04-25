# 💰 Sistema de Legalización de Gastos - SQL Server

Aplicación de escritorio en Python con integración a SQL Server para la gestión profesional de gastos empresariales.

## 🎯 Características

### ✅ Funcionalidades Principales
- Sistema de login con autenticación segura (SHA-256)
- Registro de usuarios con roles (Admin, Supervisor, Usuario)
- Gestión completa de gastos (CRUD)
- Aprobación/rechazo de gastos por administradores
- Estadísticas en tiempo real
- Auditoría completa de cambios
- Comentarios en gastos
- Reportes personalizados

### 🗄️ Integración SQL Server
- Conexión directa a SQL Server local (192.168.0.22)
- Base de datos relacional completa
- Procedimientos almacenados
- Vistas para reportes
- Triggers de auditoría
- Índices para rendimiento óptimo

## 📋 Requisitos

### Software Necesario

1. **Python 3.7 o superior**
   ```bash
   python --version
   ```

2. **Microsoft ODBC Driver para SQL Server**
   
   **Windows:**
   - Descargar desde: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
   - Instalar "ODBC Driver 17 for SQL Server"
   
   **Linux (Ubuntu/Debian):**
   ```bash
   curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
   curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
   sudo apt-get update
   sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
   sudo apt-get install -y unixodbc-dev
   ```
   
   **macOS:**
   ```bash
   brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
   brew update
   brew install msodbcsql17
   ```

3. **Paquetes Python**
   ```bash
   pip install pyodbc
   pip install tkinter  # Generalmente viene con Python
   ```

## 🚀 Instalación y Configuración

### Paso 1: Configurar SQL Server

1. **Ejecutar el script de creación de base de datos:**
   - Abrir SQL Server Management Studio (SSMS)
   - Conectar al servidor: `192.168.0.22`
   - Abrir el archivo `setup_database.sql`
   - Ejecutar el script completo (F5)
   
   Esto creará:
   - Base de datos `GastosDB`
   - Tablas: Usuarios, Gastos, Comentarios, Categorias, Auditoria
   - Vistas para reportes
   - Procedimientos almacenados
   - Usuario admin por defecto

2. **Verificar la creación:**
   ```sql
   USE GastosDB;
   SELECT * FROM Usuarios;
   SELECT * FROM Gastos;
   ```

### Paso 2: Configurar la Aplicación

1. **Editar archivo `config.py`:**
   ```python
   SQL_SERVER = '192.168.0.22'
   SQL_DATABASE = 'GastosDB'
   SQL_USERNAME = 'sa'  # Tu usuario
   SQL_PASSWORD = 'TuPassword123!'  # Tu contraseña
   ```

2. **Probar la conexión:**
   ```bash
   python config.py
   ```
   
   Deberías ver: `✅ Conexión exitosa`

### Paso 3: Ejecutar la Aplicación

```bash
python app_gastos_sqlserver.py
```

## 🔐 Credenciales por Defecto

- **Usuario:** `admin`
- **Contraseña:** `admin123`

## 📊 Estructura de la Base de Datos

### Tabla: Usuarios
```sql
- id (INT, PK, IDENTITY)
- usuario (VARCHAR, UNIQUE)
- password (VARCHAR, SHA-256)
- nombre (VARCHAR)
- rol (VARCHAR: 'admin', 'usuario', 'supervisor')
- email (VARCHAR)
- departamento (VARCHAR)
- fecha_registro (DATETIME)
- activo (BIT)
```

### Tabla: Gastos
```sql
- id (INT, PK, IDENTITY)
- usuario_id (INT, FK)
- descripcion (VARCHAR)
- monto (DECIMAL)
- categoria (VARCHAR)
- fecha_gasto (DATE)
- estado (VARCHAR: 'Pendiente', 'Aprobado', 'Rechazado')
- fecha_registro (DATETIME)
- aprobado_por (INT, FK)
- fecha_aprobacion (DATETIME)
```

### Otras Tablas
- **Comentarios:** Para notas en gastos
- **Categorias:** Catálogo de categorías
- **Auditoria:** Registro de todos los cambios

## 🎨 Uso de la Aplicación

### Para Usuarios Normales:

1. **Agregar Gasto:**
   - Completar formulario (descripción, monto, categoría, fecha)
   - Click en "💾 Agregar Gasto"
   - El gasto se registra con estado "Pendiente"

2. **Ver Mis Gastos:**
   - Tabla muestra todos los gastos propios
   - Estados visibles: Pendiente, Aprobado, Rechazado

3. **Actualizar:**
   - Click en "🔄 Actualizar" para refrescar datos

### Para Administradores:

1. **Ver Todos los Gastos:**
   - Tabla muestra gastos de todos los usuarios
   - Columna adicional con nombre del usuario

2. **Aprobar Gastos:**
   - Seleccionar un gasto de la tabla
   - Click en "✓ Aprobar"

3. **Rechazar Gastos:**
   - Seleccionar un gasto de la tabla
   - Click en "✗ Rechazar"

4. **Ver Estadísticas:**
   - Panel superior muestra:
     - Total de gastos
     - Pendientes / Aprobados / Rechazados
     - Monto total

## 🔧 Solución de Problemas

### Error: "No se pudo conectar a SQL Server"

**Causas comunes:**

1. **SQL Server no está corriendo:**
   ```bash
   # Verificar servicio en Windows
   services.msc
   # Buscar: SQL Server (MSSQLSERVER)
   ```

2. **Usuario o contraseña incorrectos:**
   - Verificar credenciales en `config.py`
   - Probar login en SSMS

3. **Firewall bloqueando puerto 1433:**
   ```bash
   # Windows: Abrir puerto 1433
   # Panel de Control > Firewall > Reglas de entrada
   # Nueva regla > Puerto > TCP > 1433
   ```

4. **SQL Server no acepta conexiones remotas:**
   - SSMS > Propiedades del Servidor
   - Conexiones > "Permitir conexiones remotas"
   - SQL Server Configuration Manager
   - TCP/IP > Habilitado

5. **Driver ODBC no instalado:**
   ```bash
   # Verificar drivers instalados
   # Windows: ODBC Data Sources (64-bit)
   # Linux: odbcinst -q -d
   ```

### Error: "No module named 'pyodbc'"

```bash
pip install pyodbc
```

### Error: "No module named 'tkinter'"

**Linux:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

## 📊 Consultas SQL Útiles

### Ver todos los gastos pendientes:
```sql
SELECT * FROM vw_GastosPendientes;
```

### Resumen por usuario:
```sql
SELECT * FROM vw_ResumenGastosPorUsuario;
```

### Reporte por período:
```sql
EXEC sp_ReporteGastosPorPeriodo 
    @fecha_inicio = '2025-01-01', 
    @fecha_fin = '2025-01-31';
```

### Total aprobado de un usuario:
```sql
SELECT dbo.fn_TotalGastosAprobados(2);
```

### Ver auditoría:
```sql
SELECT * FROM Auditoria ORDER BY fecha DESC;
```

## 🔒 Seguridad

- ✅ Contraseñas encriptadas con SHA-256
- ✅ Validación de roles y permisos
- ✅ Auditoría completa de cambios
- ✅ Triggers automáticos para rastreo
- ✅ Índices para rendimiento
- ✅ Foreign keys para integridad referencial

## 📈 Mejoras Futuras

- [ ] Exportación a Excel/PDF
- [ ] Gráficos y dashboards
- [ ] Adjuntar comprobantes (imágenes)
- [ ] Notificaciones por correo
- [ ] API REST
- [ ] Aplicación web
- [ ] Múltiples niveles de aprobación
- [ ] Presupuestos por departamento
- [ ] Integración con sistemas de contabilidad

## 🗂️ Archivos del Proyecto

```
proyecto/
├── app_gastos_sqlserver.py  # Aplicación principal
├── config.py                # Configuración
├── setup_database.sql       # Script de BD
└── README_SQLSERVER.md      # Esta documentación
```

## 🆘 Soporte

### Verificar conexión:
```bash
python config.py
```

### Verificar base de datos:
```sql
USE GastosDB;
SELECT COUNT(*) FROM Usuarios;
SELECT COUNT(*) FROM Gastos;
```

### Logs de SQL Server:
```
C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\Log\ERRORLOG
```

## 📝 Notas Importantes

1. **Backup regular:** Hacer respaldos de `GastosDB`
2. **Actualizar contraseña:** Cambiar password de `admin` en producción
3. **Configurar SSL:** Para conexiones seguras en producción
4. **Monitorear rendimiento:** Revisar índices periódicamente
5. **Auditoría:** La tabla Auditoria crece - limpiar periódicamente

## 🎓 Capacitación

### Para usuarios nuevos:
1. Crear cuenta desde pantalla de login
2. Registrar primer gasto de prueba
3. Esperar aprobación del administrador
4. Consultar estadísticas personales

### Para administradores:
1. Revisar gastos pendientes diariamente
2. Aprobar/rechazar con comentarios
3. Generar reportes mensuales
4. Monitorear usuarios y categorías

---

## 📧 Información Técnica

**Desarrollado con:**
- Python 3.x
- Tkinter (GUI)
- pyodbc (Conectividad)
- SQL Server 2016+ (Base de datos)

**Servidor SQL:** 192.168.0.22  
**Base de datos:** GastosDB  
**Puerto:** 1433 (por defecto)

---

**¡Sistema listo para producción! 🚀**
