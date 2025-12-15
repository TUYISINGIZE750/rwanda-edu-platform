@echo off
echo ========================================
echo CLEAN START - TVET SYSTEM
echo ========================================
echo.

cd backend

echo [1/4] Cleaning old database...
del app.db 2>nul
echo Done.

echo.
echo [2/4] Running fresh migration...
alembic upgrade head
if errorlevel 1 (
    echo Migration failed! Trying to fix...
    alembic stamp head
    alembic upgrade head
)

echo.
echo [3/4] Seeding TVET schools...
python seed_tvet_schools.py

echo.
echo [4/4] Starting backend on port 8080...
echo.
echo Backend: http://localhost:8080
echo API Docs: http://localhost:8080/docs
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
