@echo off
title Instalación de Dependencias - Rayogas ESP
echo.
echo ═══════════════════════════════════════════════════════
echo   INSTALACION DE DEPENDENCIAS
echo   Formulario Rayogas ESP - Puntos Colombia
echo ═══════════════════════════════════════════════════════
echo.
echo Instalando dependencias necesarias...
echo.

pip install pyodbc
pip install Pillow

echo.
echo ═══════════════════════════════════════════════════════
echo   Instalacion completada
echo ═══════════════════════════════════════════════════════
echo.
echo IMPORTANTE: Verifique que tiene instalado el driver ODBC
echo para SQL Server en su sistema.
echo.
echo Puede descargarlo de:
echo https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
echo.
pause
