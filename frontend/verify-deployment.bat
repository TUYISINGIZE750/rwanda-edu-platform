@echo off
echo ========================================
echo   TSSANYWHERE - Deployment Verification
echo ========================================
echo.

echo Testing main site...
curl -s -o nul -w "Main site status: %%{http_code}\n" https://tssanywhere.pages.dev/

echo Testing admin login...
curl -s -o nul -w "Admin login status: %%{http_code}\n" https://tssanywhere.pages.dev/admin-login

echo Testing API connectivity...
curl -s -o nul -w "Backend API status: %%{http_code}\n" https://rwanda-edu-platform.onrender.com/api/v1/health

echo.
echo ========================================
echo   Verification Complete
echo ========================================
echo.
echo If all status codes are 200, your deployment is working correctly!
echo.
pause