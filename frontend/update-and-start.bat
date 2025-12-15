@echo off
echo Updating to latest dependencies...
npm install
npm update
npm audit fix --force

echo Starting development server with latest versions...
npm run dev