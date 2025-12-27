@echo off
echo ========================================
echo DEPLOYING SCHOOLS DROPDOWN FIX
echo ========================================
echo.
echo This will build and deploy the fix to production
echo.

cd frontend

echo Building frontend...
call npm run build

echo.
echo ========================================
echo Build complete!
echo.
echo Next steps:
echo 1. Commit changes: git add . && git commit -m "Fix schools dropdown endpoint"
echo 2. Push to GitHub: git push
echo 3. Cloudflare Pages will auto-deploy
echo.
echo OR manually deploy dist folder to Cloudflare Pages
echo ========================================
pause
