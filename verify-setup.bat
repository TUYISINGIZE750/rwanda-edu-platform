@echo off
echo ========================================
echo Rwanda Education Platform - Setup Verification
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo.
echo Checking Node.js installation...
node --version
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found!
    pause
    exit /b 1
)

echo.
echo Checking backend dependencies...
cd backend
pip list | findstr fastapi
if %errorlevel% neq 0 (
    echo Installing backend dependencies...
    pip install -r requirements.txt
)

echo.
echo Checking frontend dependencies...
cd ..\frontend
if not exist node_modules (
    echo Installing frontend dependencies...
    npm install
)

echo.
echo Checking database...
cd ..\backend
if not exist app.db (
    echo Creating database...
    python -c "from app.core.database import engine; from app.models import *; Base.metadata.create_all(bind=engine)"
)

echo.
echo ========================================
echo Setup verification complete!
echo Run start-system.bat to start the application
echo ========================================
pause