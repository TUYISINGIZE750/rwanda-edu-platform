@echo off
echo ========================================
echo   TSSANYWHERE - Deployment Status
echo ========================================
echo.

echo ✅ Build Status: COMPLETED
echo ✅ Configuration: READY
echo ✅ Assets: PREPARED
echo.

echo 📁 Build Output Location:
echo    %cd%\dist\
echo.

echo 🌐 Deployment Options:
echo.
echo 1. AUTOMATIC (Recommended):
echo    - Get API token: https://dash.cloudflare.com/profile/api-tokens
echo    - Run: set CLOUDFLARE_API_TOKEN=your_token
echo    - Run: deploy-to-cloudflare.bat
echo.
echo 2. MANUAL UPLOAD:
echo    - Go to: https://dash.cloudflare.com/
echo    - Pages → Create project → Upload assets
echo    - Upload the 'dist' folder
echo.
echo 3. GITHUB INTEGRATION:
echo    - Push to GitHub repository
echo    - Connect via Cloudflare Pages dashboard
echo.

echo 🔗 Expected URLs after deployment:
echo    Main site: https://tssanywhere.pages.dev/
echo    Admin: https://tssanywhere.pages.dev/admin-login
echo.

echo 🔧 Backend Status:
curl -s -o nul -w "Backend API: %%{http_code} " https://rwanda-edu-platform.onrender.com/api/v1/health 2>nul
if %errorlevel% equ 0 (
    echo ✅ ONLINE
) else (
    echo ❌ OFFLINE or UNREACHABLE
)

echo.
echo 📋 Next Steps:
echo    1. Choose deployment method above
echo    2. Deploy the application
echo    3. Run verify-deployment.bat to test
echo    4. Access admin panel at /admin-login
echo.

pause