@echo off
chcp 65001 > nul
echo ========================================================
echo   Automatización de Git - Proyecto Club Deportivo
echo ========================================================
echo.
echo Este script creara el historial de versiones por capas
echo tal como lo solicito el profesor y lo subira a GitHub.
echo.

set /p REPO_URL="Pega la URL de tu repositorio en GitHub (ej. https://github.com/tu-usuario/repo.git) y presiona Enter: "

if "%REPO_URL%"=="" (
    echo.
    echo [ERROR] No ingresaste ninguna URL. Ejecuta el archivo nuevamente.
    pause
    exit /b
)

echo.
echo [1/6] Inicializando repositorio local...
git init
git branch -M main

echo.
echo [2/6] Creando Commit 1: Estructura inicial...
git add .gitignore README.md requirements.txt main.py test_app.py subir_github.bat
git commit -m "feat: estructura inicial y archivos base"

echo.
echo [3/6] Creando Commit 2: Base de datos y repositorios...
git add db\ models\ repositories\
git commit -m "feat: base de datos y repositorios"

echo.
echo [4/6] Creando Commit 3: Servicios de negocio...
git add services\
git commit -m "feat: servicios de negocio"

echo.
echo [5/6] Creando Commit 4: Interfaz grafica...
git add ui\
git commit -m "feat: interfaz tkinter"

echo.
echo [6/6] Conectando y subiendo a GitHub...
git remote add origin %REPO_URL%
git push -u origin main

echo.
echo ========================================================
echo ¡Proceso completado! Revisa tu repositorio en GitHub.
echo ========================================================
pause
