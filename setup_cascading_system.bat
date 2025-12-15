@echo off
echo ================================================================================
echo 🚀 SETTING UP INNOVATIVE CASCADING REGISTRATION SYSTEM
echo ================================================================================

cd /d "%~dp0"

echo.
echo [STEP 1] Setting up backend...
cd backend

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo [STEP 2] Setting up database with TVET schools...
python load_official_tvet_data.py

echo.
echo [STEP 3] Testing cascading system...
python test_cascading_system.py

echo.
echo [STEP 4] Setting up frontend...
cd ..\frontend

echo Installing Node.js dependencies...
call npm install

echo.
echo ================================================================================
echo ✅ CASCADING SYSTEM SETUP COMPLETE!
echo ================================================================================

echo.
echo 🎯 INNOVATIVE FEATURES IMPLEMENTED:
echo    • Province + District → Auto-display TVET/TSS schools
echo    • School Selection → Auto-display all trades in school
echo    • Trade Selection → Auto-display all levels (Level 1-6)
echo    • Real-time cascading without page refresh
echo    • Enhanced registration with complete student data
echo.
echo 🚀 TO START THE SYSTEM:
echo    1. Backend: cd backend && python -m uvicorn app.main:app --reload
echo    2. Frontend: cd frontend && npm run dev
echo    3. Open: http://localhost:5173/register
echo.
echo 💡 CASCADING LOGIC:
echo    Students select province/district → schools auto-display
echo    Students select school → trades auto-display  
echo    Students select trade → levels auto-display (Level 1-6)
echo    Students complete registration with full data
echo.

pause