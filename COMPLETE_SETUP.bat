@echo off
echo ============================================
echo COMPLETE SETUP - USERS + SERVERS
echo ============================================
echo.

REM Step 1: Create test users
echo [1/3] Creating test users...
cd backend
python CREATE_TEST_USERS.py
cd ..

echo.
echo [2/3] Starting Backend Server...
start "Backend Server" cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080"
timeout /t 4 /nobreak >nul

echo.
echo [3/3] Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"
timeout /t 3 /nobreak >nul

echo.
echo ============================================
echo SYSTEM READY!
echo ============================================
echo.
echo Backend:  http://localhost:8080
echo Frontend: http://localhost:5173
echo.
echo TEST CREDENTIALS:
echo ============================================
echo.
echo ADMIN (DOS):
echo   URL: http://localhost:5173/admin-login
echo   Email: admin@test.com
echo   Password: admin123
echo.
echo TEACHER:
echo   URL: http://localhost:5173/login
echo   Email: teacher@test.com
echo   Password: teacher123
echo.
echo STUDENT:
echo   URL: http://localhost:5173/login
echo   Email: student@test.com
echo   Password: student123
echo.
echo All users at: KAYENZI TVET SCHOOL (KAMONYI)
echo ============================================
echo.
echo Opening browser...
timeout /t 2 /nobreak >nul
start http://localhost:5173
echo.
pause
