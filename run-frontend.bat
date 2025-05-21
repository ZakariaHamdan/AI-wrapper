@echo off
REM run-frontend.bat
echo Starting Frontend Service...
cd /d "%~dp0frontend"
echo Executing: npm start
cmd /k "color 0B && npm start"