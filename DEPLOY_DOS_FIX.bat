@echo off
echo ========================================
echo DOS LOGIN - FINAL DEPLOYMENT
echo ========================================
echo.

:PUSH
echo Attempting to push to GitHub...
cd "f:\SIDE HUSTLE\Holidays learning\rwanda-edu-platform"
git push origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! Code pushed to GitHub
    echo ========================================
    echo.
    echo Cloudflare Pages is now deploying...
    echo Wait 1-2 minutes, then test at:
    echo https://tssanywhere.pages.dev/admin-login
    echo.
    echo Test with:
    echo Email: nyamata_tvet_school_1@tssanywhere.rw
    echo Password: dos12024
    echo.
    pause
    exit /b 0
) else (
    echo.
    echo Push failed! Network issue detected.
    echo.
    choice /C YN /M "Retry push"
    if errorlevel 2 goto MANUAL
    if errorlevel 1 goto PUSH
)

:MANUAL
echo.
echo ========================================
echo MANUAL DEPLOYMENT OPTION
echo ========================================
echo.
echo Since git push is failing, you can:
echo.
echo 1. Wait for network to stabilize and run this script again
echo.
echo 2. OR Deploy manually to Cloudflare:
echo    - Go to: https://dash.cloudflare.com/
echo    - Navigate to Pages -^> tssanywhere
echo    - Click "Create deployment"
echo    - Upload folder: frontend\dist
echo    - Click Deploy
echo.
echo 3. OR Use Cloudflare CLI (wrangler):
echo    cd frontend
echo    npx wrangler pages deploy dist
echo.
pause
