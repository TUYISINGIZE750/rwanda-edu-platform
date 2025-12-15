@echo off
echo Fixing database migration issues...
echo.

echo [1/3] Deleting old database...
del app.db 2>nul

echo [2/3] Resetting migrations...
alembic downgrade base 2>nul
alembic stamp head

echo [3/3] Creating fresh database...
alembic upgrade head

echo.
echo Database fixed! Now run: python seed_tvet_schools.py
pause
