@echo off
echo ============================================
echo SCHOOLS DROPDOWN - COMPLETE FIX
echo ============================================
echo.

echo The issue: Backend code on Render is outdated (commit 018aa8f)
echo Your local code has the fix (commit 025f423)
echo GitHub push is failing due to network issues
echo.

echo SOLUTION: Manual deployment on Render
echo.
echo Step 1: Go to https://dashboard.render.com
echo Step 2: Select "rwanda-edu-backend"
echo Step 3: Click "Manual Deploy" button
echo Step 4: Select "Deploy latest commit" 
echo         (This will pull from GitHub even if push failed)
echo.
echo OR if that doesn't work:
echo.
echo Step 1: In Render Dashboard, click "Shell" tab
echo Step 2: Run these commands:
echo.
echo   cd /opt/render/project/src
echo   git fetch origin
echo   git reset --hard origin/main
echo   exit
echo.
echo Step 3: Click "Manual Deploy" again
echo.
echo This will force Render to get the latest code from GitHub.
echo.
echo After deployment, test at:
echo https://tssanywhere.pages.dev/admin-login
echo Select: South ^> Kamonyi ^> Should show 6 schools
echo.
pause
