@echo off
echo ========================================
echo Starting Backend Server
echo ========================================
echo.
echo Server will start on: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
