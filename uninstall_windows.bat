@echo off
REM CommandBrain Uninstaller for Windows

echo ========================================
echo CommandBrain Uninstaller
echo ========================================
echo.
echo This will remove:
echo   - CommandBrain package
echo   - Database file (%%USERPROFILE%%\.commandbrain.db)
echo.
set /p CONFIRM="Are you sure you want to uninstall? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo.
    echo Uninstallation cancelled.
    exit /b 0
)

echo.
echo Uninstalling CommandBrain...
echo.

REM Uninstall the package
echo [1/2] Removing CommandBrain package...
pip uninstall -y commandbrain 2>nul
if errorlevel 1 (
    echo - Package not found (already removed?)
) else (
    echo checkmark Package removed
)
echo.

REM Remove database
echo [2/2] Removing database...
set DB_PATH=%USERPROFILE%\.commandbrain.db
if exist "%DB_PATH%" (
    del "%DB_PATH%"
    echo checkmark Database removed
) else (
    echo - Database not found (already removed?)
)

echo.
echo ========================================
echo Uninstallation Complete!
echo ========================================
echo.
echo CommandBrain has been removed from your system.
echo.
echo To reinstall later, just run: install_windows.bat
echo.
pause
