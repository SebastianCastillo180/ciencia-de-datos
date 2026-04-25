# 🚀 GUÍA DE INICIO RÁPIDO
# Sistema Web de Legalización de Gastos para Conductores

## ⚡ Inicio en 5 Pasos

### 1️⃣ Instalar Dependencias (Una sola vez)

```bash
pip install flask werkzeug pyodbc
```

### 2️⃣ Configurar SQL Server

Editar en `app.py` (líneas 19-25):

```python
SQL_CONFIG = {
    'server': '192.168.0.22',              # ⬅️ CAMBIAR: Tu servidor
    'database': 'GastosConductoresDB',
    'username': 'sa',                       # ⬅️ CAMBIAR: Tu usuario
    'password': 'TuPassword123!',          # ⬅️ CAMBIAR: Tu contraseña
    'driver': 'ODBC Driver 17 for SQL Server'
}
```

### 3️⃣ Ejecutar Aplicación

```bash
python app.py
```

Verás algo como:
```
============================================================
Sistema de Legalización de Gastos para Conductores
============================================================

Inicializando base de datos...
✅ Base de datos inicializada correctamente

✅ Sistema listo para usar

Servidor: http://localhost:5000
Usuario por defecto: ADMIN
Contraseña: admin123

============================================================
```

### 4️⃣ Abrir Navegador

Ir a: **http://localhost:5000**

### 5️⃣ Iniciar Sesión

```
Usuario: ADMIN
Contraseña: admin123
```

## ✅ ¡Listo! Ya puedes usar el sistema

---

## 📱 Funciones Principales

### Como Conductor:

1. **Registrarse:**
   - Click en "Registrarse"
   - Completar formulario
   - Crear código único (ej: COND001)

2. **Registrar Gasto:**
   - Dashboard → "Nuevo Gasto"
   - Llenar formulario
   - Guardar

3. **Ver Gastos:**
   - Sidebar → "Mis Gastos"
   - Filtrar por fecha/tipo/estado
   - Editar gastos pendientes

### Como Admin:

1. **Aprobar Gastos:**
   - Administración → "Aprobar Gastos"
   - ✓ Aprobar o ✗ Rechazar

2. **Ver Reportes:**
   - Administración → "Reportes"
   - Estadísticas por conductor
   - Estadísticas por tipo

---

## 🔧 Solución Rápida de Problemas

### ❌ Error: "No se pudo conectar a SQL Server"

✅ **Solución:**
1. Verificar que SQL Server esté corriendo
2. Revisar `SQL_CONFIG` en app.py
3. Probar conexión: `python test_conexion.py`
4. Verificar firewall (puerto 1433)

### ❌ Error: "ModuleNotFoundError: No module named 'flask'"

✅ **Solución:**
```bash
pip install flask werkzeug pyodbc
```

### ❌ No puedo aprobar gastos

✅ **Solución:**
- Solo usuarios con rol 'admin' o 'supervisor' pueden aprobar
- Usar cuenta ADMIN o cambiar rol en base de datos

### ❌ La página se ve sin estilos

✅ **Solución:**
- Verificar conexión a internet (Bootstrap desde CDN)
- Refrescar página (Ctrl + F5)

---

## 📊 Tipos de Gastos Disponibles

- 🚗 **Combustible** - Gasolina, diésel, GNV
- 💵 **Peajes** - Casetas de peaje
- 🅿️ **Parqueadero** - Estacionamientos
- 🔧 **Mantenimiento** - Reparaciones, aceite, llantas
- 🍔 **Alimentación** - Comidas durante rutas
- 🏨 **Hospedaje** - Hoteles, alojamiento
- 🧼 **Lavado** - Lavado de vehículo
- 📦 **Otros** - Otros gastos operativos

---

## 🔐 Seguridad

✅ Contraseñas encriptadas  
✅ Sesiones seguras  
✅ Control de acceso por roles  
✅ Protección SQL Injection

---

## 📞 Necesitas Ayuda?

1. **Revisar documentación completa:** `README_WEB.md`
2. **Probar conexión SQL:** `python test_conexion.py`
3. **Ver logs:** Consola donde ejecutas `python app.py`

---

## 🎯 Estructura de Archivos

```
proyecto/
├── app.py                  ⬅️ Aplicación principal (EJECUTAR ESTE)
├── README_WEB.md          ⬅️ Documentación completa
├── INICIO_RAPIDO.md       ⬅️ Esta guía
├── requirements_web.txt   ⬅️ Dependencias
├── templates/             ⬅️ Plantillas HTML
│   ├── login.html
│   ├── dashboard.html
│   ├── gastos.html
│   └── ...
└── static/                ⬅️ Archivos estáticos
    ├── css/
    └── js/
```

---

## ✨ Tips Útiles

### Cambiar Puerto (si 5000 está ocupado):
```python
# En app.py, última línea:
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Acceder desde otra PC en la red:
```
http://192.168.X.X:5000
```
(Donde X.X es la IP de tu PC)

### Crear más usuarios admin:
```sql
-- En SQL Server Management Studio
UPDATE Conductores 
SET rol = 'admin' 
WHERE codigo_conductor = 'COND001'
```

---

## 📈 Próximos Pasos

Una vez el sistema funcione:

1. ✅ Cambiar contraseña de admin
2. ✅ Registrar conductores reales
3. ✅ Configurar tipos de gastos según tu empresa
4. ✅ Establecer políticas de aprobación
5. ✅ Capacitar usuarios

---

## 🎉 ¡Todo Listo!

El sistema está completamente funcional y listo para usar.

**Acceso:** http://localhost:5000  
**Usuario:** ADMIN  
**Contraseña:** admin123

---

*Última actualización: 2025*
