@echo off
:: ============================================================
::  build_windows.bat
::  Compila generar_qr_win.py a un .exe standalone para Windows
::  Requiere: Python 3.8+ instalado y en el PATH
:: ============================================================

echo.
echo  ============================================================
echo    Compilador de QR Generator para Windows
echo  ============================================================
echo.

:: ── 1. Verificar que Python esté disponible ──────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado. Instala Python 3.8+ y volvé a intentarlo.
    echo         Descarga: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: ── 2. Instalar dependencias ─────────────────────────────────
echo [1/4] Instalando dependencias...
pip install pyinstaller qrcode Pillow lxml -q
if errorlevel 1 (
    echo [ERROR] Fallo al instalar dependencias.
    pause
    exit /b 1
)
echo       OK

:: ── 3. Limpiar compilaciones anteriores ──────────────────────
echo [2/4] Limpiando compilacion anterior...
if exist dist\generar_qr.exe del /f /q dist\generar_qr.exe
if exist build rmdir /s /q build
if exist generar_qr.spec del /f /q generar_qr.spec
echo       OK

:: ── 4. Compilar con PyInstaller ───────────────────────────────
echo [3/4] Compilando... (puede tardar 1-2 minutos)
python -m PyInstaller ^
    --onefile ^
    --console ^
    --name generar_qr ^
    --clean ^
    qr_gen_windows.py

if errorlevel 1 (
    echo.
    echo [ERROR] La compilacion fallo. Revisa los mensajes de error arriba.
    pause
    exit /b 1
)

:: ── 5. Copiar el .exe a la raiz del proyecto ─────────────────
echo [4/4] Copiando ejecutable...
copy /y dist\generar_qr.exe generar_qr.exe >nul
echo       OK

echo.
echo  ============================================================
echo   Compilacion exitosa!
echo   Ejecutable: generar_qr.exe  (en esta carpeta)
echo.
echo   Como distribuir:
echo     - Compartir solo el archivo generar_qr.exe
echo     - Tus companeros pueden arrastrar el CSV sobre el .exe
echo     - No necesitan instalar Python ni ninguna libreria
echo  ============================================================
echo.
pause
