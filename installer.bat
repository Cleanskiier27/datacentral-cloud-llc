@echo off
REM NetworkBuster Installer Launcher
REM Automatically requests Administrator privileges

setlocal enabledelayedexpansion

REM Check for admin privileges
net session >nul 2>&1
if errorlevel 1 (
    echo.
    echo ================================================================
    echo NetworkBuster Installer requires Administrator privileges
    echo ================================================================
    echo.
    echo Requesting Administrator access...
    echo.
    
    REM Re-launch as admin
    powershell -Command "Start-Process cmd -ArgumentList '/c \"%~s0\"' -Verb RunAs"
    exit /b
)

REM Run the PowerShell installer
echo.
echo ================================================================
echo NetworkBuster Windows Application Installer v1.0.0
echo ================================================================
echo.

cd /d "%~dp0"

powershell -ExecutionPolicy Bypass -File "installer.ps1"

pause
