@echo off
chcp 65001 > nul
color 0B
title 🚀 Blockchain P2P - Demo Automático

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║        🚀 BLOCKCHAIN P2P - DEMO AUTOMÁTICO                   ║
echo ║           Sistema de Pagos Descentralizado                   ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo 📋 Preparando el entorno...
echo.

REM Verificar que Python está instalado
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no está instalado o no está en el PATH
    echo.
    echo 💡 Instala Python desde: https://www.python.org/downloads/
    echo    Asegúrate de marcar "Add Python to PATH" durante la instalación
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.

REM Verificar que los archivos existen
if not exist "blockchain.py" (
    echo ❌ ERROR: No se encontró blockchain.py
    echo    Asegúrate de estar en el directorio correcto
    pause
    exit /b 1
)

if not exist "demo_automatico.py" (
    echo ❌ ERROR: No se encontró demo_automatico.py
    echo    Asegúrate de estar en el directorio correcto
    pause
    exit /b 1
)

if not exist "dashboard.html" (
    echo ⚠️  ADVERTENCIA: No se encontró dashboard.html
    echo    El dashboard no se abrirá automáticamente
    echo.
)

echo ✅ Archivos del proyecto encontrados
echo.

REM Instalar dependencias si no están instaladas
echo 📦 Verificando dependencias de Python...
echo.

python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo 📥 Instalando Flask...
    pip install flask flask-cors
)

python -c "import cryptography" 2>nul
if %errorlevel% neq 0 (
    echo 📥 Instalando Cryptography...
    pip install cryptography
)

python -c "import requests" 2>nul
if %errorlevel% neq 0 (
    echo 📥 Instalando Requests...
    pip install requests
)

echo.
echo ✅ Todas las dependencias están instaladas
echo.

REM Crear directorio para logs si no existe
if not exist "logs" mkdir logs

REM Limpiar logs anteriores
del /Q logs\*.log 2>nul

echo ═══════════════════════════════════════════════════════════════
echo.
echo 🎬 INICIANDO DEMO AUTOMÁTICO
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

REM Iniciar los 3 nodos en ventanas separadas
echo 🟢 Iniciando Nodo Alice (Puerto 5000)...
start "Alice - Puerto 5000" cmd /k "color 0A && python blockchain.py 5000"
timeout /t 3 /nobreak > nul

echo 🟡 Iniciando Nodo Bob (Puerto 5001)...
start "Bob - Puerto 5001" cmd /k "color 0E && python blockchain.py 5001"
timeout /t 3 /nobreak > nul

echo 🔵 Iniciando Nodo Charlie (Puerto 5002)...
start "Charlie - Porto 5002" cmd /k "color 0D && python blockchain.py 5002"
timeout /t 3 /nobreak > nul

echo.
echo ⏳ Esperando que los nodos se inicialicen...
timeout /t 5 /nobreak > nul

echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo ✅ Los 3 nodos están activos
echo.
echo    • Alice:   http://localhost:5000
echo    • Bob:     http://localhost:5001
echo    • Charlie: http://localhost:5002
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

REM Abrir dashboard si existe
if exist "dashboard.html" (
    echo 🌐 Abriendo Dashboard en el navegador...
    start "" "dashboard.html"
    timeout /t 2 /nobreak > nul
    echo.
)

echo 🤖 Ejecutando Demo Automático...
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

REM Ejecutar el demo automático
python demo_automatico.py

echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🎉 DEMO COMPLETADO
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 💡 Los nodos siguen ejecutándose para que explores la blockchain
echo.
echo 📊 Puedes:
echo    • Ver el dashboard: dashboard.html
echo    • Alice API: http://localhost:5000/blockchain
echo    • Bob API: http://localhost:5001/blockchain
echo    • Charlie API: http://localhost:5002/blockchain
echo.
echo 🛑 Para detener los nodos:
echo    • Cierra las ventanas de cada nodo manualmente
echo    • O presiona Ctrl+C en cada ventana
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

pause

REM Preguntar si desea cerrar los nodos
echo.
choice /C SN /M "¿Deseas cerrar todos los nodos ahora? (S=Sí, N=No)"
if errorlevel 2 (
    echo.
    echo ✅ Los nodos seguirán ejecutándose
    echo    Ciérralos manualmente cuando termines
    echo.
) else (
    echo.
    echo 🛑 Cerrando todos los nodos...
    taskkill /FI "WindowTitle eq Alice*" /F > nul 2>&1
    taskkill /FI "WindowTitle eq Bob*" /F > nul 2>&1
    taskkill /FI "WindowTitle eq Charlie*" /F > nul 2>&1
    echo ✅ Nodos cerrados
    echo.
)

echo 👋 ¡Gracias por usar la demo!
echo.
pause