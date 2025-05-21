@echo off
REM run-backend.bat
echo Starting Backend Service...
cd /d "%~dp0backend"
echo Executing: python -m app.main
cmd /k "color 0A && python -m app.main"