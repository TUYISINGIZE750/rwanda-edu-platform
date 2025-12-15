@echo off
echo ============================================
echo CLEARING BROWSER CACHE AND STARTING SERVERS
echo ============================================
echo.

REM Kill any existing Python servers on port 5175
echo [1/4] Stopping old servers...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq HTML*" 2>nul

REM Start no-cache server
echo [2/4] Starting NO-CACHE HTML server on port 5175...
start "HTML Server (NO CACHE)" cmd /k "python NO_CACHE_SERVER.py"
timeout /t 2 /nobreak >nul

REM Start backend if not running
echo [3/4] Starting Backend on port 8080...
start "Backend Server" cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080"
timeout /t 3 /nobreak >nul

REM Start frontend if not running
echo [4/4] Starting Frontend on port 5173...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo ============================================
echo SERVERS STARTED - CACHE DISABLED
echo ============================================
echo.
echo Backend:  http://localhost:8080
echo Frontend: http://localhost:5173
echo HTML:     http://localhost:5175
echo.
echo IMPORTANT: Use these steps to see changes:
echo 1. Close ALL browser tabs with localhost:5175
echo 2. Press Ctrl+Shift+Delete in browser
echo 3. Clear "Cached images and files"
echo 4. Open NEW tab: http://localhost:5175/registration.html
echo.
echo Or use INCOGNITO mode: Ctrl+Shift+N
echo ============================================
pause
