@echo off
echo ========================================
echo  E-SHURI SYSTEM - PHONE ACCESS MODE
echo ========================================
echo.

echo Step 1: Finding your IP address...
echo.
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set IP=%%a
    set IP=!IP:~1!
    echo Your IP Address: !IP!
)
echo.

echo Step 2: Starting Backend (Network Mode)...
echo.
cd backend
start cmd /k "echo BACKEND RUNNING && uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload"
timeout /t 3 >nul

echo Step 3: Starting Frontend (Network Mode)...
echo.
cd ..\frontend
start cmd /k "echo FRONTEND RUNNING && npm run dev -- --host"
timeout /t 5 >nul

echo.
echo ========================================
echo  READY TO TEST!
echo ========================================
echo.
echo ON YOUR LAPTOP:
echo   Open: http://localhost:5173
echo   Login as Teacher: Elam@gmail.com / password123
echo.
echo ON YOUR PHONE:
echo   1. Connect to SAME WiFi
echo   2. Open browser
echo   3. Go to: http://!IP!:5173
echo   4. Login as Student: teststudent1@school.rw / password123
echo.
echo Then test live audio/video sessions!
echo.
pause
