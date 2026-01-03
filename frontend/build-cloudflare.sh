#!/bin/bash
echo "Building for Cloudflare Pages..."
cp .env.cloudflare .env.production
npm ci
npm run build
echo "Build complete!"