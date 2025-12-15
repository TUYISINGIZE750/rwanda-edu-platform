@echo off
echo ========================================
echo FIXING CORS AND STARTING SERVERS
echo ========================================

REM Kill any existing processes
echo Stopping existing servers...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8080" ^| find "LISTENING"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5173" ^| find "LISTENING"') do taskkill /F /PID %%a 2>nul

timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo Starting Backend (Port 8080)
echo ========================================
cd /d "%~dp0\backend"
start "Backend Server" cmd /k "python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload"

timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo Starting Frontend (Port 5173)
echo ========================================
cd /d "%~dp0\frontend"
start "Frontend Server" cmd /k "npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo SERVERS STARTED!
echo ========================================
echo Backend: http://localhost:8080
echo Frontend: http://localhost:5173
echo.
echo Press any key to open browser...
pause >nul

start http://localhost:5173

echo.
echo Servers are running in separate windows.
echo Close those windows to stop the servers.
pause
