@echo off
echo Starting SQL Database Assistant Backend...
cd backend
python -m pip install fastapi uvicorn pyodbc pandas tenacity python-dotenv google-generativeai
uvicorn app:app --host 0.0.0.0 --port 8000 --reload