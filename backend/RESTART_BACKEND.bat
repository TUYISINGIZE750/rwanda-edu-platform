@echo off
echo ========================================
echo Restarting Backend Server (Port 8080)
echo ========================================

REM Kill any existing process on port 8080
echo Stopping any existing server on port 8080...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8080" ^| find "LISTENING"') do taskkill /F /PID %%a 2>nul

timeout /t 2 /nobreak >nul

echo Starting backend server...
cd /d "%~dp0"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

pause
