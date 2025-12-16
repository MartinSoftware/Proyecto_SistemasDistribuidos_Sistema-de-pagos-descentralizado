@echo off
chcp 65001 > nul
color 0A
title 🔗 Blockchain Demo Automático - Sistema de Pagos P2P

echo.
echo ═══════════════════════════════════════════════════════════════
echo    🚀 BLOCKCHAIN DEMO AUTOMÁTICO - SISTEMA DE PAGOS P2P
echo ═══════════════════════════════════════════════════════════════
echo.

REM Verificar si Python está instalado
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no está instalado o no está en el PATH
    echo.
    echo Por favor instala Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python detectado correctamente
echo.

REM Verificar dependencias
echo 📦 Verificando dependencias...
python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Flask no está instalado. Instalando dependencias...
    pip install flask flask-cors cryptography requests
    echo.
)

echo ✅ Todas las dependencias están listas
echo.

REM Limpiar procesos previos de Python (opcional, por si quedaron abiertos)
echo 🧹 Limpiando procesos anteriores...
taskkill /F /IM python.exe > nul 2>&1

echo.
echo ═══════════════════════════════════════════════════════════════
echo    FASE 1: INICIANDO LOS 3 NODOS
echo ═══════════════════════════════════════════════════════════════
echo.

REM Iniciar los tres nodos en ventanas separadas
echo 🟢 Iniciando nodo ALICE (Puerto 5000)...
start "🔗 NODO ALICE - Puerto 5000" cmd /k "color 0B && python blockchain.py 5000"
timeout /t 2 /nobreak > nul

echo 🟡 Iniciando nodo BOB (Puerto 5001)...
start "🔗 NODO BOB - Puerto 5001" cmd /k "color 0E && python blockchain.py 5001"
timeout /t 2 /nobreak > nul

echo 🟢 Iniciando nodo CHARLIE (Puerto 5002)...
start "🔗 NODO CHARLIE - Puerto 5002" cmd /k "color 0A && python blockchain.py 5002"
timeout /t 3 /nobreak > nul

echo.
echo ✅ Los 3 nodos están iniciándose...
echo ⏳ Esperando a que los servidores estén listos (10 segundos)...
timeout /t 10 /nobreak > nul

echo.
echo ═══════════════════════════════════════════════════════════════
echo    FASE 2: ABRIENDO DASHBOARD WEB
echo ═══════════════════════════════════════════════════════════════
echo.

REM Verificar que existe el archivo HTML
if exist "dashboard.html" (
    echo 🌐 Abriendo dashboard en el navegador...
    start "" "dashboard.html"
    timeout /t 2 /nobreak > nul
    echo ✅ Dashboard abierto
) else (
    echo ⚠️  Advertencia: No se encontró dashboard.html
    echo    Puedes abrir manualmente el archivo HTML después
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo    FASE 3: EJECUTANDO DEMO AUTOMÁTICO
echo ═══════════════════════════════════════════════════════════════
echo.
echo ⏳ Esperando 5 segundos adicionales para estabilización...
timeout /t 5 /nobreak > nul

echo.
echo 🤖 Ejecutando script de automatización de la demo...
echo.

REM Ejecutar el script Python de automatización
python demo_automatico.py

echo.
echo ═══════════════════════════════════════════════════════════════
echo    ✅ DEMO COMPLETADA
echo ═══════════════════════════════════════════════════════════════
echo.
echo 📊 Puedes ver los resultados en:
echo    • Dashboard web: http://localhost:5000 (o el archivo HTML abierto)
echo    • Nodo Alice: http://localhost:5000/blockchain
echo    • Nodo Bob: http://localhost:5001/blockchain
echo    • Nodo Charlie: http://localhost:5002/blockchain
echo.
echo 💡 Los nodos seguirán ejecutándose. Para detenerlos:
echo    1. Cierra las ventanas de los nodos, o
echo    2. Ejecuta: detener_nodos.bat
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

pause

REM Preguntar si desea detener los nodos
echo.
choice /C SN /M "¿Deseas detener los nodos ahora?"
if %errorlevel% equ 1 (
    echo.
    echo 🛑 Deteniendo todos los nodos...
    taskkill /F /IM python.exe > nul 2>&1
    echo ✅ Nodos detenidos
)

echo.
echo 👋 ¡Gracias por usar la demo!
echo.
pause