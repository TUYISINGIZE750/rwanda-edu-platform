@echo off
echo ========================================
echo Rwanda TVET Schools Setup
echo ========================================
echo.

echo [1/3] Running database migrations...
cd backend
python -m alembic upgrade head
if %errorlevel% neq 0 (
    echo ERROR: Migration failed
    pause
    exit /b 1
)
echo ✓ Migrations completed
echo.

echo [2/3] Seeding TVET schools data...
python seed_tvet_schools.py
if %errorlevel% neq 0 (
    echo ERROR: Seeding failed
    pause
    exit /b 1
)
echo ✓ Schools seeded successfully
echo.

echo [3/3] Verifying installation...
python -c "from app.core.database import SessionLocal; from app.models.school import School; db = SessionLocal(); count = db.query(School).count(); print(f'\n✓ Total schools in database: {count}'); db.close()"
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start backend: cd backend ^&^& uvicorn app.main:app --reload
echo 2. Start frontend: cd frontend ^&^& npm run dev
echo 3. Visit: http://localhost:5173/register
echo.
pause
