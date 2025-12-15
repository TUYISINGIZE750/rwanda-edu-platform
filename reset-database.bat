@echo off
echo ========================================
echo Resetting Database with Correct Schema
echo ========================================
echo.

cd backend

echo 1. Resetting database schema...
python reset_database.py

echo.
echo 2. Creating sample data...
python create_sample_data.py

echo.
echo Database reset complete!
echo You can now restart the backend server.
pause