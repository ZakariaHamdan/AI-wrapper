@echo off
REM run-all.bat
echo Starting All Services...
start cmd /k "color 0A && cd /d %~dp0backend && echo Backend Service && python -m app.main"
start cmd /k "color 0B && cd /d %~dp0frontend && echo Frontend Service && npm start"
echo All services started in separate windows.