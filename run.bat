@echo off
echo Starting full application...

start cmd /k "cd backend && python start_services.py"
timeout /t 3
start cmd /k "cd frontend && run_frontend.bat"

echo Both services started in separate windows.