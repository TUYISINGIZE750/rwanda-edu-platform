@echo off
echo ========================================
echo  Starting Frontend with Network Access
echo ========================================
echo.

cd frontend

echo.
echo Starting frontend with network access...
echo This allows access from your phone!
echo.
echo Press Ctrl+C to stop
echo.

npm run dev -- --host
