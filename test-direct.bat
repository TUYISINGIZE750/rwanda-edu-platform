@echo off
echo Testing server directly...
echo.

echo Checking if server is running on port 8000:
netstat -an | findstr :8000
echo.

echo Testing with browser-friendly URL:
start http://localhost:8000/health
echo.

echo Testing API docs:
start http://localhost:8000/docs
echo.

pause