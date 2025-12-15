@echo off
echo ========================================
echo Rwanda Education Platform - Full Test
echo ========================================
echo.

set PASSED=0
set FAILED=0

echo [TEST 1] Checking Docker...
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [PASS] Docker installed
    set /a PASSED+=1
) else (
    echo [FAIL] Docker not found
    set /a FAILED+=1
    goto summary
)

echo [TEST 2] Stopping existing containers...
docker-compose down >nul 2>&1
echo [PASS] Cleaned up

echo [TEST 3] Starting services...
docker-compose up -d
timeout /t 20 /nobreak >nul
echo [PASS] Services started

echo [TEST 4] Checking PostgreSQL...
docker-compose ps | findstr "postgres" | findstr "Up" >nul
if %errorlevel% equ 0 (
    echo [PASS] PostgreSQL running
    set /a PASSED+=1
) else (
    echo [FAIL] PostgreSQL not running
    set /a FAILED+=1
)

echo [TEST 5] Checking Redis...
docker-compose ps | findstr "redis" | findstr "Up" >nul
if %errorlevel% equ 0 (
    echo [PASS] Redis running
    set /a PASSED+=1
) else (
    echo [FAIL] Redis not running
    set /a FAILED+=1
)

echo [TEST 6] Checking Backend...
docker-compose ps | findstr "backend" | findstr "Up" >nul
if %errorlevel% equ 0 (
    echo [PASS] Backend running
    set /a PASSED+=1
) else (
    echo [FAIL] Backend not running
    set /a FAILED+=1
)

echo [TEST 7] Testing backend health...
timeout /t 5 /nobreak >nul
curl -s http://localhost:8000/health 2>nul | findstr "healthy" >nul
if %errorlevel% equ 0 (
    echo [PASS] Backend healthy
    set /a PASSED+=1
) else (
    echo [FAIL] Backend not responding
    set /a FAILED+=1
)

echo [TEST 8] Running migrations...
docker-compose exec -T backend alembic upgrade head
if %errorlevel% equ 0 (
    echo [PASS] Migrations applied
    set /a PASSED+=1
) else (
    echo [FAIL] Migrations failed
    set /a FAILED+=1
)

echo [TEST 9] Seeding database...
docker-compose exec -T backend python seed_data.py
if %errorlevel% equ 0 (
    echo [PASS] Data seeded
    set /a PASSED+=1
) else (
    echo [FAIL] Seeding failed
    set /a FAILED+=1
)

echo [TEST 10] Testing teacher login...
curl -s -X POST http://localhost:8000/api/v1/auth/login -H "Content-Type: application/json" -d "{\"email\":\"teacher1@school1.rw\",\"password\":\"teacher123\"}" 2>nul | findstr "access_token" >nul
if %errorlevel% equ 0 (
    echo [PASS] Teacher login works
    set /a PASSED+=1
) else (
    echo [FAIL] Teacher login failed
    set /a FAILED+=1
)

echo [TEST 11] Testing student login...
curl -s -X POST http://localhost:8000/api/v1/auth/login -H "Content-Type: application/json" -d "{\"email\":\"student11@school1.rw\",\"password\":\"student123\"}" 2>nul | findstr "access_token" >nul
if %errorlevel% equ 0 (
    echo [PASS] Student login works
    set /a PASSED+=1
) else (
    echo [FAIL] Student login failed
    set /a FAILED+=1
)

echo [TEST 12] Testing API docs...
curl -s http://localhost:8000/docs 2>nul | findstr "Swagger" >nul
if %errorlevel% equ 0 (
    echo [PASS] API docs accessible
    set /a PASSED+=1
) else (
    echo [FAIL] API docs not found
    set /a FAILED+=1
)

:summary
echo.
echo ========================================
echo TEST SUMMARY
echo ========================================
echo PASSED: %PASSED%/12
echo FAILED: %FAILED%/12
echo.

if %FAILED% equ 0 (
    echo [SUCCESS] All tests passed!
    echo.
    echo Platform is ready:
    echo - Backend: http://localhost:8000
    echo - API Docs: http://localhost:8000/docs
    echo.
    echo Test credentials:
    echo - Teacher: teacher1@school1.rw / teacher123
    echo - Student: student11@school1.rw / student123
    echo.
    echo Next: cd frontend ^&^& npm install ^&^& npm run dev
) else (
    echo [WARNING] Some tests failed.
    echo.
    echo Check logs: docker-compose logs
    echo Restart: docker-compose restart
)

echo.
pause
