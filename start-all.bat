@echo off
echo ========================================
echo Rwanda Education Platform - Start All
echo ========================================
echo.

echo Cleaning up...
docker-compose down -v >nul 2>&1

echo [1/5] Starting Docker services...
docker-compose up -d
timeout /t 20 /nobreak >nul
echo [DONE] Services started

echo [2/5] Running migrations...
docker-compose exec -T backend alembic upgrade head
echo [DONE] Migrated

echo [3/5] Seeding database...
docker-compose exec -T backend python seed_data.py
echo [DONE] Seeded

echo [4/5] Installing frontend...
cd frontend
if not exist node_modules call npm install
echo [DONE] Frontend ready

echo [5/5] Starting frontend...
start cmd /k "npm run dev"
cd ..
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo RWANDA EDU PLATFORM - READY!
echo ========================================
echo.
echo TECH STACK:
echo - Backend:  FastAPI + SQLAlchemy 2.x + Pydantic v2
echo - Frontend: Vue 3 + Vite + Pinia + Tailwind CSS
echo - Database: PostgreSQL 15
echo - Cache:    Redis 7
echo - PWA:      Service Worker + IndexedDB
echo - i18n:     vue-i18n (Kinyarwanda/English/French)
echo.
echo ACCESS POINTS:
echo - Backend API:  http://localhost:8080
echo - API Docs:     http://localhost:8080/docs
echo - Frontend:     http://localhost:5173
echo - PostgreSQL:   localhost:5435
echo - Redis:        localhost:6381
echo.
echo TEST CREDENTIALS:
echo - Teacher: teacher1@school1.rw / teacher123
echo - Student: student11@school1.rw / student123
echo.
echo Opening browser...
start http://localhost:8080/docs
timeout /t 1 /nobreak >nul
start http://localhost:5173
echo.
pause
