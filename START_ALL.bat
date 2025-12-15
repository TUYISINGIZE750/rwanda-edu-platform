@echo off
echo ============================================
echo Starting Rwanda EDU Platform
echo ============================================
echo.

start "Backend Server" cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080"
timeout /t 3 /nobreak >nul

start "Frontend Server" cmd /k "cd frontend && npm run dev"
timeout /t 2 /nobreak >nul

start "HTML Server (No Cache)" cmd /k "python NO_CACHE_SERVER.py"

echo.
echo ============================================
echo All servers started!
echo ============================================
echo Backend:  http://localhost:8080
echo Frontend: http://localhost:5173
echo HTML:     http://localhost:5175
echo.
