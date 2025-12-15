@echo off
echo Checking what's running on port 8000...
netstat -ano | findstr :8000
echo.

echo Testing endpoints:
echo.
echo Health:
curl http://localhost:8000/health
echo.
echo.

echo Docs:
curl http://localhost:8000/docs
echo.
echo.

echo All routes:
curl http://localhost:8000/openapi.json
echo.

pause