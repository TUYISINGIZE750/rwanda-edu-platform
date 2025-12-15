@echo off
echo ========================================
echo FINAL COMPLETE START - PORT 8080
echo ========================================

cd backend

echo [1/3] Recreating database...
del app.db 2>nul
python create_db_direct.py

echo.
echo [2/3] Loading real TVET data...
python load_real_tvet_data.py

echo.
echo [3/3] Starting server on port 8080...
echo Backend: http://localhost:8080
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
