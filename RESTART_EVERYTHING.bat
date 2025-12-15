@echo off
echo ========================================
echo RESTART COMPLETE SYSTEM
echo ========================================
echo.
echo This will:
echo   1. Setup backend database
echo   2. Start backend server
echo   3. Start frontend server
echo   4. Run authentication tests
echo.
pause

cd backend

echo.
echo [1/4] Setting up backend database...
echo ========================================
call alembic upgrade head
if errorlevel 1 (
    echo ERROR: Migration failed!
    pause
    exit /b 1
)

echo.
echo [2/4] Seeding TVET schools...
echo ========================================
call python seed_tvet_schools.py
if errorlevel 1 (
    echo ERROR: Seeding failed!
    pause
    exit /b 1
)

echo.
echo [3/4] Starting backend server...
echo ========================================
echo Backend will run on http://localhost:8080
start "Backend Server" cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080"

timeout /t 5 /nobreak >nul

cd ..\frontend

echo.
echo [4/4] Starting frontend...
echo ========================================
echo Frontend will run on http://localhost:5173
start "Frontend Server" cmd /k "npm run dev"

timeout /t 5 /nobreak >nul

cd ..

echo.
echo ========================================
echo SYSTEM STARTED SUCCESSFULLY!
echo ========================================
echo.
echo Backend:  http://localhost:8080
echo API Docs: http://localhost:8080/docs
echo Frontend: http://localhost:5173
echo.
echo Opening test script in 3 seconds...
timeout /t 3 /nobreak >nul

cd backend
start "Auth Tests" cmd /k "python test_auth_endpoints.py"

echo.
echo All services are running!
echo Close this window when done testing.
pause
