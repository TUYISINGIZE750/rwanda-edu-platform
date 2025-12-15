@echo off
echo ============================================
echo Starting Rwanda EDU Platform
echo ============================================
echo.

cd /d "%~dp0"

echo [1/3] Checking database...
cd backend
python -c "import sqlite3; conn = sqlite3.connect('app.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM schools'); count = cursor.fetchone()[0]; print(f'Schools in database: {count}'); conn.close()"

if errorlevel 1 (
    echo ERROR: Database check failed!
    pause
    exit /b 1
)

echo.
echo [2/3] Starting Backend Server (Port 8080)...
start "Backend Server" cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080"

timeout /t 5 /nobreak >nul

echo.
echo [3/3] Starting Frontend Server...
cd ..\frontend
start "Frontend Server" cmd /k "npm run dev"

echo.
echo ============================================
echo Both servers are starting!
echo ============================================
echo Backend:  http://localhost:8080
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8080/docs
echo.
echo Press any key to close this window...
pause >nul
