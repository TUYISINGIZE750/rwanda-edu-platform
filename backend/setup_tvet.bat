@echo off
echo ========================================
echo TVET Registration System Setup
echo ========================================
echo.

echo [1/4] Installing required packages...
pip install pandas openpyxl
echo.

echo [2/4] Running database migration...
alembic upgrade head
echo.

echo [3/4] Loading TVET schools from Excel...
python load_official_tvet_data.py
echo.

echo [4/4] Testing integration...
python test_tvet_integration.py
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo You can now start the server with:
echo   python -m uvicorn app.main:app --reload
echo.
pause
