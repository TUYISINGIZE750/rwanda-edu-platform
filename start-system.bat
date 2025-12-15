
@echo off
echo ========================================
echo Rwanda Education Platform - Full System Start
echo ========================================
echo.

echo 1. Setting up database and sample data...
cd backend
python create_sample_data.py

echo.
echo 2. Starting Backend Server...
start "Backend Server" cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080"
timeout /t 3

echo.
echo 3. Starting Frontend Development Server...
cd ..\frontend
start "Frontend Server" cmd /k "npm run dev"
timeout /t 3

echo.
echo 4. System Status:
echo - Backend: http://localhost:8080
echo - Frontend: http://localhost:5173
echo - API Docs: http://localhost:8080/docs
echo.

echo 5. Testing API Health...
timeout /t 5
curl -X GET "http://localhost:8080/health" -H "accept: application/json"
echo.

echo.
echo ========================================
echo System is starting up...
echo Please wait for both servers to fully load
echo Then open http://localhost:5173 in your browser
echo ========================================
pause