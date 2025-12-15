@echo off
echo ========================================
echo Starting Backend Server on Port 8080
echo ========================================
cd /d "%~dp0"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
pause
