@echo off
echo ========================================
echo REAL TVET DATA - PORT 8080
echo ========================================

cd backend

echo [1/3] Deleting old database...
del app.db 2>nul

echo [2/3] Loading REAL Excel data...
python load_real_tvet_data.py

echo.
echo [3/3] Starting server on port 8080...
echo Backend: http://localhost:8080
echo API Docs: http://localhost:8080/docs
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
