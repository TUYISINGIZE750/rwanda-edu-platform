@echo off
echo Testing Rwanda Education Platform Authentication...
echo.

echo Starting backend server...
cd backend
start /B python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
timeout /t 5

echo.
echo Testing API endpoints...
curl -X GET "http://localhost:8000/health" -H "accept: application/json"
echo.

echo Testing locations endpoint...
curl -X GET "http://localhost:8000/api/v1/api/locations/provinces" -H "accept: application/json"
echo.

echo Backend is running on http://localhost:8000
echo Frontend should be started separately with: npm run dev
echo.
pause