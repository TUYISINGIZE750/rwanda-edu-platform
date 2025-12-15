@echo off
echo Fixing frontend npm issue...
cd frontend
del package-lock.json 2>nul
rmdir /s /q node_modules 2>nul
echo Installing dependencies...
call npm install --force
echo Done! Now run: npm run dev
pause
