@echo off
:: ─────────────────────────────────────────────────────────
:: CommandBrain Windows Installer v2.0
:: ─────────────────────────────────────────────────────────
setlocal

echo.
echo   ╔════════════════════════════════════════════════╗
echo   ║        CommandBrain Installer v2.0             ║
echo   ╚════════════════════════════════════════════════╝
echo.

:: Check Python
where python >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] Python not found!
    echo   Download from: https://python.org/downloads
    echo   IMPORTANT: Check "Add to PATH" during install.
    exit /b 1
)
echo   [OK] Python found

:: Install with pip
echo   --^>^> Installing CommandBrain...
pip install . -q 2>nul
if errorlevel 1 (
    echo   [FAIL] pip install failed
    echo   Try:  python -m pip install .
    exit /b 1
)
echo   [OK] CommandBrain installed

:: Initialize database
echo.
set /p KALI="  Include Kali security tools? (y/n) [y]: "
if "%KALI%"=="" set KALI=y

if /i "%KALI%"=="y" (
    cb --setup --kali
) else (
    cb --setup
)

echo.
echo   ╔════════════════════════════════════════════════╗
echo   ║        Installation Complete!                  ║
echo   ╚════════════════════════════════════════════════╝
echo.
echo   Try:  cb ssh
echo         cb password cracking
echo         cb --help
echo.
pause
