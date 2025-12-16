@echo off
chcp 65001 > nul
color 0C
title 🛑 Detener Nodos Blockchain

echo.
echo ═══════════════════════════════════════════════════════════════
echo    🛑 DETENIENDO TODOS LOS NODOS BLOCKCHAIN
echo ═══════════════════════════════════════════════════════════════
echo.

echo 🔍 Buscando procesos de Python...
echo.

REM Listar procesos de Python activos
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" >nul

if %errorlevel% equ 0 (
    echo ✅ Procesos de Python encontrados
    echo.
    echo 🛑 Cerrando todos los procesos de Python...
    taskkill /F /IM python.exe >nul 2>&1
    
    if %errorlevel% equ 0 (
        echo.
        echo ✅ Todos los nodos han sido detenidos correctamente
    ) else (
        echo.
        echo ⚠️  Algunos procesos no pudieron ser cerrados
        echo    Intenta cerrarlos manualmente desde el Administrador de tareas
    )
) else (
    echo.
    echo ℹ️  No se encontraron procesos de Python en ejecución
    echo    Los nodos ya están detenidos
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo.

pause