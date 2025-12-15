#!/bin/bash

echo "🇷🇼 Rwanda Education Platform - Deployment Script"
echo "=================================================="

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "❌ Docker required"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose required"; exit 1; }

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for database
echo "⏳ Waiting for database..."
sleep 10

# Run migrations
echo "📊 Running database migrations..."
docker-compose exec -T backend alembic upgrade head

# Seed data
echo "🌱 Seeding pilot data (10 schools)..."
docker-compose exec -T backend python seed_data.py

# Check health
echo "🏥 Health check..."
curl -f http://localhost:8000/health || { echo "❌ Backend health check failed"; exit 1; }

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📍 Backend API: http://localhost:8000"
echo "📍 Frontend: http://localhost:5173"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "🔑 Default credentials:"
echo "   Teacher: teacher1@school1.rw / teacher123"
echo "   Student: student11@school1.rw / student123"
echo ""
echo "📚 Read DEPLOYMENT.md for production deployment"
