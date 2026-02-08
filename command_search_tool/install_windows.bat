@echo off
REM CommandBrain Easy Installer for Windows
REM This script sets up CommandBrain automatically

echo ========================================
echo CommandBrain Windows Installer
echo ========================================
echo.
echo Checking prerequisites...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ================================================================
    echo   PYTHON NOT FOUND!
    echo ================================================================
    echo.
    echo CommandBrain requires Python 3.6 or higher.
    echo.
    echo HOW TO INSTALL PYTHON:
    echo.
    echo 1. Go to: https://www.python.org/downloads/
    echo    (Copy this link or search "download python")
    echo.
    echo 2. Click the big yellow "Download Python" button
    echo.
    echo 3. Run the installer
    echo.
    echo 4. IMPORTANT: Check the box that says:
    echo    [X] Add Python to PATH
    echo    (This is at the BOTTOM of the first screen!)
    echo.
    echo 5. Click "Install Now"
    echo.
    echo 6. Restart your computer (important!)
    echo.
    echo 7. Run this installer again
    echo.
    echo ================================================================
    echo.
    echo TROUBLESHOOTING:
    echo - If you just installed Python, restart your computer first
    echo - Open a NEW command prompt after installing Python
    echo - Verify by typing: python --version
    echo.
    echo Need help? Ask your instructor!
    echo ================================================================
    echo.
    pause
    exit /b 1
)

echo [1/4] Python found!
python --version
echo.

echo [2/4] Installing CommandBrain...
pip install -e .
if errorlevel 1 (
    echo ERROR: Installation failed
    pause
    exit /b 1
)
echo.

echo [3/4] Setting up database...
commandbrain-setup
if errorlevel 1 (
    echo ERROR: Database setup failed
    pause
    exit /b 1
)
echo.
echo Database created with ~30 essential Linux commands!
echo.

echo [4/5] Enabling purpose-based search...
echo.
echo Adding student-friendly slang terms (brute force, network scan, etc.)
python enhance_slang_tags.py >nul 2>&1
echo Student can now search by purpose/task!
echo.

echo [5/5] OPTIONAL: Add Kali Security Tools?
echo.
echo Kali tools include: nmap, metasploit, burpsuite, sqlmap, etc.
echo These are for SECURITY PROFESSIONALS and PENTESTERS only.
echo.
echo If you just need basic Linux commands, type 'n'
echo.
set /p KALI="Add Kali security tools? (y/n): "
if /i "%KALI%"=="y" (
    echo.
    echo Adding 30+ Kali tools...
    commandbrain-kali
    echo Kali tools added!
) else (
    echo.
    echo Skipping Kali tools. You can add them later with: commandbrain-kali
)
echo.

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo You now have the 'cb' command available!
echo.
echo Try it out:
echo   cb ssh                    # Search for ssh
echo   cb network monitoring     # Multi-word search  
echo   cb -d grep                # Detailed view
echo   cb --list                 # List categories
echo.
echo It's that simple! Just type: cb ANYTHING
echo.
pause
