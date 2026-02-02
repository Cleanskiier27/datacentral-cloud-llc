@echo off
REM NetworkBuster Installer - Run as Administrator
REM This batch file runs the installer with elevated privileges

powershell -Command "Start-Process powershell -Verb RunAs -ArgumentList '-NoExit', '-ExecutionPolicy', 'Bypass', '-File', '%~dp0installer.ps1'"
pause
