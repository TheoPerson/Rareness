@echo off
echo ================================================================
echo   Rareness v0.3 - Windows Build Script
echo ================================================================
echo.

echo [1/2] Checking administrator privileges...
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Running as Administrator
) else (
    echo [ERROR] Administrator privileges required!
    echo.
    echo Right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo [2/2] Building desktop app...
echo.

cd /d "%~dp0"
call npm run desktop:build

if %errorLevel% == 0 (
    echo.
    echo ================================================================
    echo   BUILD SUCCESS!
    echo ================================================================
    echo.
    echo Your .exe is ready at:
    echo   packages\desktop\release\Rareness-0.3.0-Portable.exe
    echo.
    start "" "packages\desktop\release"
) else (
    echo.
    echo ================================================================
    echo   BUILD FAILED - See errors above
    echo ================================================================
    echo.
)

pause
