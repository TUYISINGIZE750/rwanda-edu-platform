#!/bin/bash

# Rwanda Education Platform - Keep-Alive Deployment Script
# This script can be deployed on any cloud platform to keep your Render server awake

set -e  # Exit on any error

echo "🚀 Deploying Rwanda Education Platform Keep-Alive Service"
echo "================================================="

# Create deployment directory
mkdir -p keep-alive-deploy
cd keep-alive-deploy

# Copy the enhanced keep-alive script
cp ../enhanced_keep_alive.py . 2>/dev/null || echo "⚠️  enhanced_keep_alive.py not found in parent directory"

# Create requirements.txt for the keep-alive service
echo "📝 Creating requirements.txt..."
cat > requirements.txt << EOF
requests>=2.28.0
aiohttp>=3.8.0
EOF

# Create Procfile for Railway/Heroku deployment
echo "📝 Creating Procfile..."
cat > Procfile << EOF
worker: python enhanced_keep_alive.py
EOF

# Create railway.toml for Railway deployment
echo "📝 Creating railway.toml..."
cat > railway.toml << EOF
[build]
builder = "nixpacks"

[deploy]
startCommand = "python enhanced_keep_alive.py"
EOF

# Create Dockerfile for containerized deployment
echo "📝 Creating Dockerfile..."
cat > Dockerfile << EOF
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY enhanced_keep_alive.py .

CMD ["python", "enhanced_keep_alive.py"]
EOF

# Create docker-compose for local testing
echo "📝 Creating docker-compose.yml..."
cat > docker-compose.yml << EOF
version: '3.8'
services:
  keep-alive:
    build: .
    restart: unless-stopped
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - ./logs:/app/logs
EOF

# Create systemd service file for VPS deployment
echo "📝 Creating systemd service file..."
cat > rwanda-keep-alive.service << EOF
[Unit]
Description=Rwanda Education Platform Keep-Alive Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/rwanda-keep-alive
ExecStart=/usr/bin/python3 enhanced_keep_alive.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create deployment instructions
echo "📝 Creating deployment instructions..."
cat > DEPLOYMENT_INSTRUCTIONS.md << EOF
# Rwanda Education Platform - Keep-Alive Service Deployment

## Quick Deploy Options

### 1. Railway (Recommended - Free Tier)
\`\`\`bash
railway login
railway link
railway up
\`\`\`

### 2. Render (Web Service)
- Connect your GitHub repo
- Set build command: \`pip install -r requirements.txt\`
- Set start command: \`python enhanced_keep_alive.py\`

### 3. Fly.io (Free Tier)
\`\`\`bash
fly launch
fly deploy
\`\`\`

### 4. Docker (Any VPS)
\`\`\`bash
docker build -t rwanda-keep-alive .
docker run -d --restart unless-stopped rwanda-keep-alive
\`\`\`

### 5. VPS with systemd
\`\`\`bash
# Copy files to /opt/rwanda-keep-alive/
sudo cp rwanda-keep-alive.service /etc/systemd/system/
sudo systemctl enable rwanda-keep-alive
sudo systemctl start rwanda-keep-alive
\`\`\`

### 6. GitHub Codespaces (Free)
- Fork this repo
- Open in Codespaces
- Run: \`python enhanced_keep_alive.py\`

### 7. Replit (Free)
- Import this project to Replit
- Run the enhanced_keep_alive.py

## Environment Variables (Optional)
- \`BACKEND_URL\`: Override default backend URL
- \`PING_INTERVAL\`: Override ping interval (seconds)
- \`LOG_LEVEL\`: Set logging level (INFO, DEBUG, WARNING)

## Testing Locally
\`\`\`bash
python enhanced_keep_alive.py
\`\`\`

EOF

# Create quick deployment scripts
echo "📝 Creating quick deployment scripts..."

cat > deploy_railway.sh << EOF
#!/bin/bash
echo "🚀 Deploying to Railway..."
railway login
railway link
railway up
echo "✅ Deployed to Railway!"
EOF
chmod +x deploy_railway.sh

cat > deploy_docker.sh << EOF
#!/bin/bash
echo "🚀 Building and running Docker container..."
docker build -t rwanda-keep-alive .
docker run -d --name rwanda-keep-alive --restart unless-stopped rwanda-keep-alive
echo "✅ Docker container running!"
EOF
chmod +x deploy_docker.sh

echo "✅ Keep-Alive deployment files created!"
echo ""
echo "📁 Files created in ./keep-alive-deploy/:"
echo "  ✓ requirements.txt"
echo "  ✓ Procfile"
echo "  ✓ railway.toml"
echo "  ✓ Dockerfile"
echo "  ✓ docker-compose.yml"
echo "  ✓ rwanda-keep-alive.service"
echo "  ✓ DEPLOYMENT_INSTRUCTIONS.md"
echo "  ✓ deploy_railway.sh"
echo "  ✓ deploy_docker.sh"
echo ""
echo "🚀 Quick Start: cd keep-alive-deploy && ./deploy_railway.sh"
echo "💡 Deploy on multiple platforms for redundancy!"
echo "🎯 Target URL: https://rwanda-edu-platform.onrender.com"