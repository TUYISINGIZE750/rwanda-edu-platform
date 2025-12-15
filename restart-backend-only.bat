@echo off
echo ========================================
echo Restarting Backend Server (No DB Reset)
echo ========================================

echo 1. Killing existing Python processes...
taskkill /f /im python.exe 2>nul
taskkill /f /im uvicorn.exe 2>nul

echo 2. Waiting for processes to close...
timeout /t 3

echo 3. Starting backend server...
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

pause
