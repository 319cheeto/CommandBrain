@echo off
REM Quick test to verify CommandBrain installation
REM Run this after installing to make sure everything works

echo ========================================
echo Testing CommandBrain Installation
echo ========================================
echo.

REM Test 1: Check if cb command exists
echo [Test 1/3] Checking if 'cb' command exists...
where cb >nul 2>&1
if errorlevel 1 (
    echo   X FAILED - 'cb' command not found
    echo.
    echo   This means the installation did not complete properly.
    echo   Try running install_windows.bat again.
    echo.
    goto :failed
) else (
    echo   ✓ PASSED - 'cb' command found
)
echo.

REM Test 2: Check if database exists
echo [Test 2/3] Checking if database exists...
if exist "%USERPROFILE%\.commandbrain.db" (
    echo   ✓ PASSED - Database found
) else (
    echo   X FAILED - Database not found at: %USERPROFILE%\.commandbrain.db
    echo.
    echo   Run: commandbrain-setup
    echo   Or: install_windows.bat
    echo.
    goto :failed
)
echo.

REM Test 3: Try searching for a command
echo [Test 3/3] Testing actual search...
cb ssh >nul 2>&1
if errorlevel 1 (
    echo   X FAILED - Search command failed
    echo.
    goto :failed
) else (
    echo   ✓ PASSED - Search works!
)
echo.

echo ========================================
echo ✅ ALL TESTS PASSED!
echo ========================================
echo.
echo CommandBrain is working correctly!
echo.
echo Try these commands:
echo   cb ssh
echo   cb find files
echo   cb network scan
echo   cb --help
echo.
goto :end

:failed
echo ========================================
echo ❌ INSTALLATION INCOMPLETE
echo ========================================
echo.
echo Please run: install_windows.bat
echo.
echo If problems persist, check TROUBLESHOOTING.md
echo.

:end
pause
