@echo off
echo ========================================
echo SCHOOLS DROPDOWN - QUICK TEST
echo ========================================
echo.
echo This will verify the schools dropdown fix is working
echo.
pause

cd backend
echo.
echo Running test script...
echo.
python TEST_SCHOOLS_DROPDOWN.py

echo.
echo ========================================
echo Test complete!
echo.
echo To start the system:
echo 1. Run: START_BACKEND.bat
echo 2. Run: START_FRONTEND.bat
echo 3. Go to: http://localhost:5173/register
echo ========================================
pause
