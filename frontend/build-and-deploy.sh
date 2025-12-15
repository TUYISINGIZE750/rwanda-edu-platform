#!/bin/bash

# Build frontend
echo "Building frontend..."
cd frontend
npm install
npm run build

# Check if build succeeded
if [ ! -d "dist" ]; then
  echo "Build failed!"
  exit 1
fi

echo "Frontend built successfully!"
echo "Ready to deploy to Cloudflare Pages"
echo ""
echo "Next steps:"
echo "1. Commit changes: git add . && git commit -m 'Build update'"
echo "2. Push to GitHub: git push origin main"
echo "3. Cloudflare will auto-deploy from GitHub"
