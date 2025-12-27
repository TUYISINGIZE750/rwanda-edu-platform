@echo off
echo ========================================
echo CLEANING DUPLICATE SCHOOLS ON RENDER
echo ========================================
echo.
echo Waiting for Render to deploy (2 minutes)...
timeout /t 120 /nobreak
echo.
echo Calling cleanup endpoint...
curl -X POST https://rwanda-edu-platform.onrender.com/api/v1/admin/remove-duplicate-schools
echo.
echo.
echo ========================================
echo Done! Test at: https://tssanywhere.pages.dev/register
echo ========================================
pause
