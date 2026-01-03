@echo off
echo ========================================
echo SCHOOLS DROPDOWN FIX DEPLOYMENT
echo ========================================
echo.

echo Step 1: Trying to push to GitHub...
git add .
git commit -m "Fix schools dropdown - case sensitivity issue"
git push origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo SUCCESS! Pushed to GitHub.
    echo Render will auto-deploy in ~2 minutes.
    echo.
    echo Test at: https://tssanywhere.pages.dev/admin-login
    echo Select: South ^> Kamonyi ^> Should show 6 schools
    pause
    exit /b 0
)

echo.
echo GitHub push failed. Manual deployment needed.
echo.
echo MANUAL DEPLOYMENT INSTRUCTIONS:
echo ================================
echo.
echo Option 1: Render Dashboard
echo 1. Go to: https://dashboard.render.com
echo 2. Select: rwanda-edu-backend
echo 3. Click: Manual Deploy ^> Deploy latest commit
echo.
echo Option 2: Direct File Update
echo 1. Go to Render Dashboard ^> Shell
echo 2. Run: nano app/api/locations.py
echo 3. Find line 145 (the schools query)
echo 4. Change: func.lower(province_name) to province_name.lower()
echo 5. Change: func.lower(district_name) to district_name.lower()
echo 6. Save and restart
echo.
echo The fixed file is saved as: locations_FIXED.py
echo You can copy its contents to Render.
echo.
pause
