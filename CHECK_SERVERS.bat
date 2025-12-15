@echo off
echo ========================================
echo CHECKING SERVER STATUS
echo ========================================
echo.

echo Checking Backend (Port 8080)...
netstat -an | find ":8080" | find "LISTENING" >nul
if %errorlevel% equ 0 (
    echo ✓ Backend is RUNNING on port 8080
) else (
    echo ✗ Backend is NOT running on port 8080
)

echo.
echo Checking Frontend (Port 5173)...
netstat -an | find ":5173" | find "LISTENING" >nul
if %errorlevel% equ 0 (
    echo ✓ Frontend is RUNNING on port 5173
) else (
    echo ✗ Frontend is NOT running on port 5173
)

echo.
echo ========================================
echo Testing Backend Connection...
echo ========================================
curl -s http://localhost:8080/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Backend is responding
    curl -s http://localhost:8080/health
) else (
    echo ✗ Backend is not responding
)

echo.
echo ========================================
echo Testing Registration API...
echo ========================================
curl -s http://localhost:8080/api/v1/registration/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Registration API is responding
    curl -s http://localhost:8080/api/v1/registration/health
) else (
    echo ✗ Registration API is not responding
)

echo.
echo ========================================
echo.
pause
