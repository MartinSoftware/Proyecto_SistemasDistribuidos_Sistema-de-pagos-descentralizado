@echo off
chcp 65001 > nul
color 0B
title 🔍 Verificador de Requisitos - Blockchain Demo

echo.
echo ═══════════════════════════════════════════════════════════════
echo    🔍 VERIFICADOR DE REQUISITOS DEL SISTEMA
echo ═══════════════════════════════════════════════════════════════
echo.

set ALL_OK=1

REM Verificar Python
echo [1/5] Verificando Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
    echo    ✅ Python instalado: %PYTHON_VER%
) else (
    echo    ❌ Python NO está instalado
    echo       Descarga desde: https://www.python.org/downloads/
    set ALL_OK=0
)

REM Verificar pip
echo [2/5] Verificando pip...
pip --version >nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ pip está disponible
) else (
    echo    ❌ pip NO está disponible
    set ALL_OK=0
)

REM Verificar Flask
echo [3/5] Verificando Flask...
python -c "import flask; print('Flask', flask.__version__)" 2>nul
if %errorlevel% equ 0 (
    echo    ✅ Flask instalado
) else (
    echo    ⚠️  Flask NO está instalado
    echo       Se instalará automáticamente al ejecutar la demo
)

REM Verificar cryptography
echo [4/5] Verificando cryptography...
python -c "import cryptography" 2>nul
if %errorlevel% equ 0 (
    echo    ✅ cryptography instalado
) else (
    echo    ⚠️  cryptography NO está instalado
    echo       Se instalará automáticamente al ejecutar la demo
)

REM Verificar archivos necesarios
echo [5/5] Verificando archivos del proyecto...
set FILES_OK=1

if exist "blockchain.py" (
    echo    ✅ blockchain.py encontrado
) else (
    echo    ❌ blockchain.py NO encontrado
    set FILES_OK=0
    set ALL_OK=0
)

if exist "demo_automatico.py" (
    echo    ✅ demo_automatico.py encontrado
) else (
    echo    ❌ demo_automatico.py NO encontrado
    set FILES_OK=0
    set ALL_OK=0
)

if exist "dashboard.html" (
    echo    ✅ dashboard.html encontrado
) else (
    echo    ⚠️  dashboard.html NO encontrado
    echo       El dashboard no se abrirá automáticamente
)

REM Verificar puertos disponibles
echo.
echo ═══════════════════════════════════════════════════════════════
echo    🔌 VERIFICANDO PUERTOS NECESARIOS
echo ═══════════════════════════════════════════════════════════════
echo.

netstat -ano | findstr ":5000 " >nul 2>&1
if %errorlevel% equ 0 (
    echo    ⚠️  Puerto 5000 está OCUPADO
    echo       Debes liberar este puerto antes de ejecutar la demo
    set ALL_OK=0
) else (
    echo    ✅ Puerto 5000 disponible (Alice)
)

netstat -ano | findstr ":5001 " >nul 2>&1
if %errorlevel% equ 0 (
    echo    ⚠️  Puerto 5001 está OCUPADO
    echo       Debes liberar este puerto antes de ejecutar la demo
    set ALL_OK=0
) else (
    echo    ✅ Puerto 5001 disponible (Bob)
)

netstat -ano | findstr ":5002 " >nul 2>&1
if %errorlevel% equ 0 (
    echo    ⚠️  Puerto 5002 está OCUPADO
    echo       Debes liberar este puerto antes de ejecutar la demo
    set ALL_OK=0
) else (
    echo    ✅ Puerto 5002 disponible (Charlie)
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo    📊 RESUMEN
echo ═══════════════════════════════════════════════════════════════
echo.

if %ALL_OK% equ 1 (
    echo    ✅✅✅ TODO LISTO PARA EJECUTAR LA DEMO ✅✅✅
    echo.
    echo    Puedes ejecutar: demo_automatico.bat
    echo.
) else (
    echo    ⚠️  FALTAN ALGUNOS REQUISITOS
    echo.
    echo    Por favor, soluciona los problemas indicados arriba
    echo.
    
    if %FILES_OK% equ 0 (
        echo    💡 ARCHIVOS FALTANTES:
        echo       Asegúrate de tener todos los archivos del proyecto
        echo       en el mismo directorio.
        echo.
    )
    
    echo    💡 PARA INSTALAR DEPENDENCIAS:
    echo       pip install flask flask-cors cryptography requests
    echo.
)

echo ═══════════════════════════════════════════════════════════════
echo.

pause