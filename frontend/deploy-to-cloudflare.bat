@echo off
echo ========================================
echo   TSSANYWHERE - Cloudflare Deployment
echo ========================================
echo.

echo Step 1: Building the application...
call npm run build:cloudflare
if %errorlevel% neq 0 (
    echo Build failed! Please check the errors above.
    pause
    exit /b 1
)

echo.
echo Step 2: Copying configuration files...
copy _headers dist\_headers >nul 2>&1
copy _redirects dist\_redirects >nul 2>&1

echo.
echo Step 3: Deploying to Cloudflare Pages...
echo.
echo IMPORTANT: You need to set your Cloudflare API token first!
echo.
echo To get your API token:
echo 1. Go to https://dash.cloudflare.com/profile/api-tokens
echo 2. Click "Create Token"
echo 3. Use "Custom token" template
echo 4. Add permissions: Zone:Zone:Read, Zone:Page Rules:Edit, Account:Cloudflare Pages:Edit
echo 5. Copy the token and run: set CLOUDFLARE_API_TOKEN=your_token_here
echo.

if "%CLOUDFLARE_API_TOKEN%"=="" (
    echo ERROR: CLOUDFLARE_API_TOKEN environment variable is not set!
    echo Please set it using: set CLOUDFLARE_API_TOKEN=your_token_here
    echo Then run this script again.
    pause
    exit /b 1
)

echo Deploying with Wrangler...
npx wrangler pages deploy dist --project-name=tssanywhere --compatibility-date=2024-01-01

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   DEPLOYMENT SUCCESSFUL!
    echo ========================================
    echo.
    echo Your site should be available at:
    echo https://tssanywhere.pages.dev
    echo.
    echo Admin login: https://tssanywhere.pages.dev/admin-login
    echo.
) else (
    echo.
    echo Deployment failed! Please check the errors above.
)

pause