@echo off
echo ========================================
echo  Starting Backend with Network Access
echo ========================================
echo.

cd backend

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Starting backend on 0.0.0.0:8080...
echo This allows access from your phone!
echo.
echo Press Ctrl+C to stop
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
