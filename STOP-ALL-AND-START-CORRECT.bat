@echo off
echo ========================================
echo STOPPING ALL SERVERS AND STARTING CORRECT ONE
echo ========================================
echo.

echo Step 1: Killing ALL Python processes...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM node.exe /T 2>nul
timeout /t 3

echo.
echo Step 2: Navigating to correct directory...
cd /d "c:\Users\PC\Music\Holidays learning\rwanda-edu-platform\backend"

echo.
echo Step 3: Starting Rwanda Education Platform backend...
python working_server.py

pause