@echo off
echo ========================================
echo Restarting Backend Server Completely
echo ========================================

echo 1. Killing any existing Python processes...
taskkill /f /im python.exe 2>nul
taskkill /f /im uvicorn.exe 2>nul

echo 2. Waiting for processes to close...
timeout /t 2

echo 3. Resetting database...
cd backend
python reset_database.py

echo 4. Creating sample data...
python create_sample_data.py

echo 5. Starting fresh backend server...
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

pause