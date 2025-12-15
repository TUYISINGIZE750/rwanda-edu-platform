@echo off
echo ============================================
echo CREATING TEST USERS
echo ============================================
echo.

cd backend
python CREATE_TEST_USERS.py

echo.
echo ============================================
echo READY TO TEST!
echo ============================================
echo.
echo You can now login with:
echo.
echo 1. ADMIN: admin@test.com / admin123
echo    Login at: http://localhost:5173/admin-login
echo.
echo 2. TEACHER: teacher@test.com / teacher123
echo    Login at: http://localhost:5173/login
echo.
echo 3. STUDENT: student@test.com / student123
echo    Login at: http://localhost:5173/login
echo.
echo All users are at KAYENZI TVET SCHOOL in KAMONYI
echo ============================================
pause
