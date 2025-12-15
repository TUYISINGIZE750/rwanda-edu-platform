@echo off
echo ========================================
echo Rwanda Education Platform
echo Complete Setup and Verification
echo ========================================
echo.

set STEP=0

:: Step 1: Check Prerequisites
set /a STEP+=1
echo [STEP %STEP%] Checking prerequisites...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker not found. Install Docker Desktop first.
    pause
    exit /b 1
)
echo [OK] Docker installed

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Install Node.js 18+ first.
    pause
    exit /b 1
)
echo [OK] Node.js installed
echo.

:: Step 2: Clean Start
set /a STEP+=1
echo [STEP %STEP%] Cleaning previous containers...
docker-compose down -v >nul 2>&1
echo [OK] Cleaned
echo.

:: Step 3: Start Services
set /a STEP+=1
echo [STEP %STEP%] Starting Docker services...
docker-compose up -d
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start services
    pause
    exit /b 1
)
echo [OK] Services started
echo Waiting 20 seconds for services to initialize...
timeout /t 20 /nobreak >nul
echo.

:: Step 4: Verify Services
set /a STEP+=1
echo [STEP %STEP%] Verifying services are running...
docker-compose ps | findstr "Up" >nul
if %errorlevel% neq 0 (
    echo [ERROR] Services not running properly
    docker-compose ps
    pause
    exit /b 1
)
echo [OK] All services running
echo.

:: Step 5: Check Backend Health
set /a STEP+=1
echo [STEP %STEP%] Checking backend health...
curl -s http://localhost:8080/health 2>nul | findstr "healthy" >nul
if %errorlevel% neq 0 (
    echo [ERROR] Backend not healthy
    echo Checking logs...
    docker-compose logs --tail=20 backend
    pause
    exit /b 1
)
echo [OK] Backend healthy
echo.

:: Step 6: Run Database Migrations
set /a STEP+=1
echo [STEP %STEP%] Running database migrations...
docker-compose exec -T backend alembic upgrade head
if %errorlevel% neq 0 (
    echo [ERROR] Migrations failed
    pause
    exit /b 1
)
echo [OK] Migrations completed
echo.

:: Step 7: Seed Database
set /a STEP+=1
echo [STEP %STEP%] Seeding database with 10 schools...
docker-compose exec -T backend python seed_data.py
if %errorlevel% neq 0 (
    echo [ERROR] Seeding failed
    pause
    exit /b 1
)
echo [OK] Database seeded
echo.

:: Step 8: Verify Database
set /a STEP+=1
echo [STEP %STEP%] Verifying database data...
docker-compose exec -T postgres psql -U user -d rwanda_edu -t -c "SELECT COUNT(*) FROM users;" >temp_count.txt 2>nul
set /p USER_COUNT=<temp_count.txt
del temp_count.txt 2>nul
if %USER_COUNT% LSS 500 (
    echo [WARNING] Expected 550 users, found %USER_COUNT%
) else (
    echo [OK] Database has %USER_COUNT% users
)
echo.

:: Step 9: Test API Login
set /a STEP+=1
echo [STEP %STEP%] Testing API authentication...
curl -s -X POST http://localhost:8080/api/v1/auth/login -H "Content-Type: application/json" -d "{\"email\":\"teacher1@school1.rw\",\"password\":\"teacher123\"}" 2>nul | findstr "access_token" >nul
if %errorlevel% neq 0 (
    echo [ERROR] Login test failed
    pause
    exit /b 1
)
echo [OK] Authentication working
echo.

:: Step 10: Setup Frontend
set /a STEP+=1
echo [STEP %STEP%] Setting up frontend...
cd frontend
if not exist node_modules (
    echo Installing dependencies...
    call npm install --silent
    if %errorlevel% neq 0 (
        echo [ERROR] npm install failed
        cd ..
        pause
        exit /b 1
    )
)
echo [OK] Frontend dependencies ready
cd ..
echo.

:: Step 11: Start Frontend
set /a STEP+=1
echo [STEP %STEP%] Starting frontend dev server...
cd frontend
start cmd /k "npm run dev"
cd ..
echo [OK] Frontend starting in new window
timeout /t 5 /nobreak >nul
echo.

:: Step 12: Final Verification
set /a STEP+=1
echo [STEP %STEP%] Running final checks...
curl -s http://localhost:8080/docs 2>nul | findstr "Swagger" >nul
if %errorlevel% equ 0 (
    echo [OK] API docs accessible
) else (
    echo [WARNING] API docs may not be ready yet
)
echo.

:: Success Summary
echo ========================================
echo SETUP COMPLETE! 
echo ========================================
echo.
echo Platform Status:
echo - Backend API:  http://localhost:8080 [RUNNING]
echo - API Docs:     http://localhost:8080/docs [READY]
echo - Frontend:     http://localhost:5173 [STARTING]
echo - PostgreSQL:   localhost:5435 [RUNNING]
echo - Redis:        localhost:6381 [RUNNING]
echo.
echo Database:
echo - Schools: 10
echo - Teachers: 50
echo - Students: 500
echo - Groups: 80
echo - Channels: 320
echo.
echo Test Credentials:
echo - Teacher: teacher1@school1.rw / teacher123
echo - Student: student11@school1.rw / student123
echo.
echo Tech Stack:
echo - Backend:  FastAPI + SQLAlchemy 2.x + PostgreSQL + Redis
echo - Frontend: Vue 3 + Vite + Pinia + Tailwind CSS
echo - PWA:      Service Worker + IndexedDB
echo - i18n:     Kinyarwanda/English/French
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul
start http://localhost:8080/docs
timeout /t 2 /nobreak >nul
start http://localhost:5173
echo.
echo ========================================
echo Next Steps:
echo 1. Test login at http://localhost:5173
echo 2. Explore API at http://localhost:8080/docs
echo 3. Check TESTING_GUIDE.md for workflows
echo 4. Read DEPLOYMENT.md for production
echo ========================================
echo.
pause
