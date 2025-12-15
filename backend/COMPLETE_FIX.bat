@echo off
echo ========================================
echo COMPLETE DATABASE FIX
echo ========================================
echo.

echo Stopping any running servers...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo [1/5] Deleting database and migrations...
del app.db 2>nul
rd /s /q alembic\versions 2>nul
mkdir alembic\versions

echo [2/5] Creating single migration...
python -c "from app.core.database import Base, engine; Base.metadata.create_all(engine); print('Database created')"

echo [3/5] Stamping as head...
alembic stamp head

echo [4/5] Seeding schools...
python seed_tvet_schools.py

echo [5/5] Starting server on port 8080...
echo.
echo Backend: http://localhost:8080
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
