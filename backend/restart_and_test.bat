@echo off
echo ========================================
echo RESTART AND TEST COMPLETE SYSTEM
echo ========================================
echo.

echo [1/5] Installing dependencies...
pip install -r requirements.txt
echo.

echo [2/5] Running database migration...
alembic upgrade head
if errorlevel 1 (
    echo ERROR: Migration failed!
    pause
    exit /b 1
)
echo.

echo [3/5] Seeding TVET schools...
python seed_tvet_schools.py
if errorlevel 1 (
    echo ERROR: Seeding failed!
    pause
    exit /b 1
)
echo.

echo [4/5] Testing complete registration flow...
python test_complete_flow.py
if errorlevel 1 (
    echo ERROR: Tests failed!
    pause
    exit /b 1
)
echo.

echo [5/5] Starting backend server...
echo.
echo ========================================
echo Backend server starting on http://localhost:8000
echo ========================================
echo.
echo API Documentation: http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
