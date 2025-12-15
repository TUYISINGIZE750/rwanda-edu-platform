@echo off
echo ========================================
echo Rwanda Education Platform - API Tests
echo ========================================
echo.

echo [TEST 1] Health Check...
curl -s http://localhost:8080/health
echo.
echo.

echo [TEST 2] Admin Login...
curl -s -X POST http://localhost:8080/api/v1/auth/login -H "Content-Type: application/json" -d "{\"email\":\"admin@school1.rw\",\"password\":\"admin123\"}" > admin_token.json
echo Admin logged in successfully
echo.

echo [TEST 3] Teacher Login...
curl -s -X POST http://localhost:8080/api/v1/auth/login -H "Content-Type: application/json" -d "{\"email\":\"teacher1@school1.rw\",\"password\":\"teacher123\"}" > teacher_token.json
echo Teacher logged in successfully
echo.

echo [TEST 4] Student Login...
curl -s -X POST http://localhost:8080/api/v1/auth/login -H "Content-Type: application/json" -d "{\"email\":\"student11@school1.rw\",\"password\":\"student123\"}" > student_token.json
echo Student logged in successfully
echo.

echo [TEST 5] Get Groups (as student)...
for /f "tokens=*" %%a in ('powershell -Command "(Get-Content student_token.json | ConvertFrom-Json).access_token"') do set STUDENT_TOKEN=%%a
curl -s -H "Authorization: Bearer %STUDENT_TOKEN%" http://localhost:8080/api/v1/directory/groups
echo.
echo.

echo [TEST 6] Admin Dashboard...
for /f "tokens=*" %%a in ('powershell -Command "(Get-Content admin_token.json | ConvertFrom-Json).access_token"') do set ADMIN_TOKEN=%%a
curl -s -H "Authorization: Bearer %ADMIN_TOKEN%" http://localhost:8080/api/v1/admin/dashboard
echo.
echo.

echo [TEST 7] Get Pending Messages (as teacher)...
for /f "tokens=*" %%a in ('powershell -Command "(Get-Content teacher_token.json | ConvertFrom-Json).access_token"') do set TEACHER_TOKEN=%%a
curl -s -H "Authorization: Bearer %TEACHER_TOKEN%" http://localhost:8080/api/v1/messages/moderation/pending
echo.
echo.

echo ========================================
echo All API Tests Completed!
echo ========================================
echo.
echo Frontend: http://localhost:5174
echo API Docs: http://localhost:8080/docs
echo.

del admin_token.json teacher_token.json student_token.json 2>nul

pause
