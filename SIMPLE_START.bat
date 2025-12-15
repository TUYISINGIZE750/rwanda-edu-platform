@echo off
echo ========================================
echo SIMPLE START - PORT 8080
echo ========================================

cd backend

echo [1/3] Creating database...
python create_db_direct.py

echo.
echo [2/3] Seeding schools...
python seed_tvet_schools.py

echo.
echo [3/3] Starting server...
echo Backend: http://localhost:8080
echo API Docs: http://localhost:8080/docs
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
