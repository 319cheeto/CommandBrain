@echo off
REM CommandBrain Updater for Windows

echo ========================================
echo CommandBrain Updater
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python first.
    pause
    exit /b 1
)

echo [1/3] Checking for updates...

REM Check if we're in a git repository
if exist ".git" (
    echo    Git repository detected
    
    REM Check if git is available
    git --version >nul 2>&1
    if errorlevel 1 (
        echo    WARNING: Git not found - skipping code update
        echo    Installing package update only...
    ) else (
        echo    Pulling latest changes...
        git pull origin main 2>nul || git pull origin master 2>nul
        if errorlevel 1 (
            echo    WARNING: Could not pull updates
            echo    Continuing with package reinstall...
        ) else (
            echo    checkmark Code updated
        )
    )
) else (
    echo    Not a git repository - skipping code update
    echo    (Proceeding with package reinstall)
)

echo.
echo [2/3] Updating CommandBrain package...
pip install --upgrade -e .
if errorlevel 1 (
    echo ERROR: Update failed
    pause
    exit /b 1
)
echo    checkmark Package updated
echo.

echo [3/3] Database is preserved (your commands are safe!)
echo.

REM Count commands in database
set DB_PATH=%USERPROFILE%\.commandbrain.db
if exist "%DB_PATH%" (
    echo    Your database is intact
)

echo.
echo ========================================
echo Update Complete!
echo ========================================
echo.
echo CommandBrain has been updated to the latest version.
echo.
echo Try it: cb ssh
echo.
pause
