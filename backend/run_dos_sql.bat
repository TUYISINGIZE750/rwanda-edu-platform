@echo off
echo ========================================
echo Adding DOS Users to Render Database
echo ========================================
echo.
echo INSTRUCTIONS:
echo 1. You need PostgreSQL client (psql) installed
echo 2. Get your PSQL command from Render dashboard
echo 3. Replace the command below with your actual PSQL command
echo.
echo ========================================
echo.

REM Replace this with your actual PSQL command from Render
set PSQL_CMD=psql "postgresql://rwanda_edu_db_user:YOUR_PASSWORD@dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com/rwanda_edu_db"

echo Running SQL file...
%PSQL_CMD% -f insert_dos_users.sql

echo.
echo ========================================
echo Done! Check output above for any errors
echo ========================================
pause
