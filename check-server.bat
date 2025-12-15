@echo off
echo Checking if backend server is running...
echo.

echo Testing health endpoint:
curl -X GET "http://localhost:8000/health" -H "accept: application/json"
echo.
echo.

echo Testing API docs:
curl -X GET "http://localhost:8000/docs" -H "accept: text/html"
echo.
echo.

echo Testing root endpoint:
curl -X GET "http://localhost:8000/" -H "accept: application/json"
echo.

pause