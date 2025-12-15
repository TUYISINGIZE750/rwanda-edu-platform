@echo off
echo ============================================
echo STARTING FRESH - NO CACHE
echo ============================================
echo.

REM Kill all existing servers
echo [1/3] Stopping all servers...
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *Server*" 2>nul
timeout /t 2 /nobreak >nul

REM Start Backend
echo [2/3] Starting Backend (Port 8080)...
start "Backend Server" cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080"
timeout /t 4 /nobreak >nul

REM Start Frontend
echo [3/3] Starting Frontend (Port 5173)...
start "Frontend Server" cmd /k "cd frontend && npm run dev"
timeout /t 3 /nobreak >nul

echo.
echo ============================================
echo SERVERS RUNNING - HOT RELOAD ENABLED
echo ============================================
echo.
echo Backend:  http://localhost:8080
echo Frontend: http://localhost:5173
echo.
echo ✅ Hot-reload enabled - Changes auto-refresh!
echo ✅ PWA cache disabled - Always fresh files!
echo.
echo Open: http://localhost:5173
echo ============================================
pause
