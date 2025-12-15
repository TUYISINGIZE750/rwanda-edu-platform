@echo off
echo ========================================
echo Test Authentication with Live Server
echo ========================================
echo.
echo This will test student and teacher registration/login
echo Make sure the server is running in another terminal
echo.
echo If server is not running, open another terminal and run:
echo   start_server.bat
echo.
pause
echo.
python test_auth_endpoints.py
echo.
pause
