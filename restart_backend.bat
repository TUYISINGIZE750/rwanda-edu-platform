@echo off
echo Stopping existing Python processes...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak >nul

echo Starting backend server...
cd backend
start cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080"

echo Backend restarted! Check the new window.
pause
