@echo off
echo ========================================
echo Rwanda Education Platform - Latest Version Startup
echo ========================================

cd "c:\Users\PC\Music\Holidays learning\rwanda-edu-platform\frontend"

echo Checking for dependency updates...
npm outdated

echo.
echo Updating to latest versions...
npm update

echo.
echo Fixing any security issues...
npm audit fix

echo.
echo Starting development server with latest versions...
echo Server will be available at: http://localhost:5173/
echo.

npm run dev

pause