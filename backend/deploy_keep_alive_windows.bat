@echo off
echo 🚀 Deploying Rwanda Education Platform Keep-Alive Service
echo =================================================

REM Create deployment directory
if not exist "keep-alive-deploy" mkdir keep-alive-deploy
cd keep-alive-deploy

REM Copy the enhanced keep-alive script if it exists
if exist "..\enhanced_keep_alive.py" (
    copy "..\enhanced_keep_alive.py" .
) else (
    echo ⚠️ enhanced_keep_alive.py not found in parent directory
)

REM Create requirements.txt
echo 📝 Creating requirements.txt...
echo requests>=2.28.0> requirements.txt
echo aiohttp>=3.8.0>> requirements.txt

REM Create Procfile for Railway/Heroku deployment
echo 📝 Creating Procfile...
echo worker: python enhanced_keep_alive.py> Procfile

REM Create railway.toml for Railway deployment
echo 📝 Creating railway.toml...
(
echo [build]
echo builder = "nixpacks"
echo.
echo [deploy]
echo startCommand = "python enhanced_keep_alive.py"
) > railway.toml

REM Create Dockerfile
echo 📝 Creating Dockerfile...
(
echo FROM python:3.9-slim
echo.
echo WORKDIR /app
echo.
echo COPY requirements.txt .
echo RUN pip install --no-cache-dir -r requirements.txt
echo.
echo COPY enhanced_keep_alive.py .
echo.
echo CMD ["python", "enhanced_keep_alive.py"]
) > Dockerfile

REM Create docker-compose.yml
echo 📝 Creating docker-compose.yml...
(
echo version: '3.8'
echo services:
echo   keep-alive:
echo     build: .
echo     restart: unless-stopped
echo     environment:
echo       - PYTHONUNBUFFERED=1
echo     volumes:
echo       - ./logs:/app/logs
) > docker-compose.yml

REM Create deployment instructions
echo 📝 Creating deployment instructions...
(
echo # Rwanda Education Platform - Keep-Alive Service Deployment
echo.
echo ## Quick Deploy Options
echo.
echo ### 1. Railway ^(Recommended - Free Tier^)
echo ```bash
echo railway login
echo railway link
echo railway up
echo ```
echo.
echo ### 2. Render ^(Web Service^)
echo - Connect your GitHub repo
echo - Set build command: `pip install -r requirements.txt`
echo - Set start command: `python enhanced_keep_alive.py`
echo.
echo ### 3. Docker ^(Any VPS^)
echo ```bash
echo docker build -t rwanda-keep-alive .
echo docker run -d --restart unless-stopped rwanda-keep-alive
echo ```
echo.
echo ## Testing Locally
echo ```bash
echo python enhanced_keep_alive.py
echo ```
) > DEPLOYMENT_INSTRUCTIONS.md

echo ✅ Keep-Alive deployment files created!
echo.
echo 📁 Files created in ./keep-alive-deploy/:
echo   ✓ requirements.txt
echo   ✓ Procfile
echo   ✓ railway.toml
echo   ✓ Dockerfile
echo   ✓ docker-compose.yml
echo   ✓ DEPLOYMENT_INSTRUCTIONS.md
echo.
echo 🚀 Quick Start: Deploy to Railway or other platforms
echo 💡 Deploy on multiple platforms for redundancy!
echo 🎯 Target URL: https://rwanda-edu-platform.onrender.com

pause