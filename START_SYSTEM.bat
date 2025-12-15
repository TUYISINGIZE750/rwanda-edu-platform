@echo off
echo ========================================
echo RWANDA EDU PLATFORM - TVET SYSTEM
echo ========================================
echo.

cd backend

echo [1/3] Running migration...
call alembic upgrade head
if errorlevel 1 (
    echo ERROR: Migration failed!
    pause
    exit /b 1
)

echo.
echo [2/3] Seeding TVET schools...
call python seed_tvet_schools.py

echo.
echo [3/3] Starting servers...
echo.
echo Backend:  http://localhost:8080
echo API Docs: http://localhost:8080/docs
echo Frontend: http://localhost:5173
echo.

start "Backend Server (Port 8080)" cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080"

timeout /t 3 /nobreak >nul

cd ..\frontend
start "Frontend Server" cmd /k "npm run dev"

timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo SYSTEM STARTED!
echo ========================================
echo.
echo Backend:  http://localhost:8080
echo Frontend: http://localhost:5173
echo.
echo Opening test in 3 seconds...
timeout /t 3 /nobreak >nul

cd ..\backend
start cmd /k "python test_auth_endpoints.py"

echo.
echo All services running!
pause
