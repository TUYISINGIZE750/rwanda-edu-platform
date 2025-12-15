@echo off
echo ========================================
echo Testing Schools API Endpoint
echo ========================================
echo.
echo Testing: Kigali city - GASABO district
curl "http://localhost:8080/api/v1/registration/schools/Kigali%%20city/GASABO"
echo.
echo.
echo Testing: East - BUGESERA district
curl "http://localhost:8080/api/v1/registration/schools/East/BUGESERA"
echo.
echo.
pause
