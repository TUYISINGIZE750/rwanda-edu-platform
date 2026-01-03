# TSSANYWHERE - Manual Cloudflare Pages Deployment Guide

## Quick Deployment Steps

### Method 1: Using Wrangler CLI (Recommended)

1. **Set your Cloudflare API Token:**
   ```bash
   set CLOUDFLARE_API_TOKEN=your_token_here
   ```

2. **Run the deployment script:**
   ```bash
   deploy-to-cloudflare.bat
   ```

### Method 2: Manual Upload via Dashboard

1. **Build the project:**
   ```bash
   npm run build:cloudflare
   ```

2. **Go to Cloudflare Dashboard:**
   - Visit: https://dash.cloudflare.com/
   - Navigate to "Pages" section
   - Click "Create a project"
   - Choose "Upload assets"

3. **Upload the dist folder:**
   - Drag and drop the entire `dist` folder
   - Project name: `tssanywhere`
   - Click "Deploy site"

### Method 3: GitHub Integration (Best for continuous deployment)

1. **Push code to GitHub repository**
2. **Connect to Cloudflare Pages:**
   - Go to Cloudflare Pages
   - Click "Connect to Git"
   - Select your repository
   - Build settings:
     - Build command: `npm run build:cloudflare`
     - Build output directory: `dist`
     - Root directory: `frontend`

## Environment Variables

Make sure these are set in Cloudflare Pages:
- `VITE_API_URL`: `https://rwanda-edu-platform.onrender.com/api/v1`
- `VITE_WS_URL`: `wss://rwanda-edu-platform.onrender.com`

## Verification

After deployment, test these URLs:
- Main site: https://tssanywhere.pages.dev/
- Admin login: https://tssanywhere.pages.dev/admin-login
- Registration: https://tssanywhere.pages.dev/register

## Troubleshooting

- If build fails: Check Node.js version (should be 18+)
- If API calls fail: Verify backend is running on Render
- If routing issues: Check `_redirects` file is in dist folder

## Current Status

✅ Build completed successfully
✅ Configuration files copied
⏳ Awaiting deployment to Cloudflare Pages

Run `verify-deployment.bat` after deployment to test everything is working.