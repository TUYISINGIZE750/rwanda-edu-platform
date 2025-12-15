@echo off
echo Stopping all Python processes...
taskkill /f /im python.exe 2>nul
timeout /t 2

echo Starting working server...
cd backend
python -m uvicorn working_server:app --reload --host 0.0.0.0 --port 8000

pause