@echo off
echo Monitoring backend health for 20 minutes...
echo Backend: https://rwanda-edu-platform.onrender.com/health
echo.

for /L %%i in (1,1,20) do (
    echo [%%i/20] Checking at %time%...
    curl -s https://rwanda-edu-platform.onrender.com/health
    echo.
    timeout /t 60 /nobreak >nul
)

echo.
echo Monitoring complete! If all checks returned healthy, keep-alive is working.
pause
