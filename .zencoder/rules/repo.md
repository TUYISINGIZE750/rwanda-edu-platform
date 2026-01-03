---
description: Repository Information Overview
alwaysApply: true
---

# TSSANYWHERE - Rwanda Education Platform

## Summary
TSSANYWHERE (Technical Skills & Learning - Anytime, Anywhere) is Rwanda's premier digital learning platform for TVET and TSS students. The platform enables continuous technical education across 165 schools in all 5 provinces of Rwanda with real-time communication, live video sessions, and offline-first architecture designed for low-bandwidth 3G networks.

## Repository Structure
- **frontend/** - Vue 3 PWA application with offline-first capabilities
- **backend/** - FastAPI REST API with WebSocket support
- **backend/app/** - Main application code (api, core, models, schemas, services)
- **backend/alembic/** - Database migration scripts
- **backend/keep-alive-deploy/** - Service monitoring and keep-alive utility
- **data/** - Rwanda locations data (provinces, districts, sectors, cells, villages)
- **rwanda-locations-json-master/** - Rwanda location registration system
- **.github/workflows/** - CI/CD automation
- **assets/** - Static resources and media files

## Projects

### Frontend (Vue 3 PWA)

**Configuration File**: `frontend/package.json`

#### Language & Runtime
**Language**: JavaScript (ES2015+)  
**Runtime**: Node.js 18+  
**Build System**: Vite  
**Package Manager**: npm

#### Dependencies
**Main Dependencies**:
- `vue@latest` - Progressive JavaScript framework
- `vue-router@latest` - Official router
- `pinia@latest` - State management
- `axios@latest` - HTTP client
- `socket.io-client@^4.7.4` - Real-time WebSocket communication
- `tailwindcss@^3.4.0` - Utility-first CSS framework
- `vue-i18n@latest` - Internationalization (Kinyarwanda, English, French)
- `@jitsi/react-sdk@^1.4.4` - Live video sessions integration
- `idb@latest` - IndexedDB wrapper for offline storage

**Development Dependencies**:
- `@vitejs/plugin-vue@latest` - Vite Vue plugin
- `vite@latest` - Build tool
- `vite-plugin-pwa@latest` - PWA capabilities

#### Build & Installation
```bash
cd frontend
npm install
npm run dev              # Development server (port 5173)
npm run build            # Production build
npm run build:cloudflare # Cloudflare Pages build
npm run preview          # Preview production build
```

#### Main Files
**Entry Point**: `frontend/src/main.js`  
**Application Root**: `frontend/src/App.vue`  
**Router**: `frontend/src/router/`  
**Configuration**: `frontend/vite.config.js`, `frontend/tailwind.config.js`

---

### Backend (FastAPI)

**Configuration File**: `backend/requirements.txt`

#### Language & Runtime
**Language**: Python  
**Version**: 3.11.7 (specified in `.python-version` and `runtime.txt`)  
**Framework**: FastAPI  
**ASGI Server**: Uvicorn  
**Package Manager**: pip

#### Dependencies
**Main Dependencies**:
- `fastapi==0.104.1` - Modern Python web framework
- `uvicorn[standard]==0.24.0` - ASGI server
- `sqlalchemy==2.0.23` - SQL toolkit and ORM
- `alembic==1.13.0` - Database migration tool
- `pydantic==2.5.0` - Data validation
- `psycopg2-binary==2.9.9` - PostgreSQL adapter
- `redis==5.0.0` - Redis client for caching and pub/sub
- `python-jose[cryptography]==3.3.0` - JWT token handling
- `passlib[bcrypt]==1.7.4` - Password hashing
- `websockets==12.0` - WebSocket support
- `httpx==0.25.2` - Async HTTP client
- `aiofiles==23.2.1` - Async file I/O
- `reportlab==4.0.9` - PDF generation

#### Build & Installation
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload  # Development
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000  # Production
```

#### Docker
**Dockerfile**: `backend/Dockerfile`  
**Base Image**: `python:3.11-slim`  
**Exposed Port**: 8000  
**Configuration**:
- Multi-stage build with system dependencies (gcc, postgresql-client)
- Gunicorn with Uvicorn workers for production
- Default configuration: 4 workers

**Docker Compose**: `docker-compose.yml`  
**Services**:
- **postgres** - PostgreSQL 15 (port 5435:5432) with optimized settings
- **redis** - Redis 7 (port 6381:6379) with LRU eviction policy
- **backend** - FastAPI application (port 8080:8000)

**Compose Commands**:
```bash
docker-compose up -d          # Start all services
docker-compose down           # Stop all services
docker-compose logs backend   # View backend logs
```

#### Main Files
**Entry Point**: `backend/app/main.py`  
**Configuration**: `backend/app/core/config.py`, `backend/.env.example`  
**Gunicorn Config**: `backend/gunicorn_config.py`  
**Database Migrations**: `backend/alembic/` (Alembic framework)

**Core Structure**:
- `backend/app/api/` - API route handlers (auth, chat, groups, messages, etc.)
- `backend/app/models/` - SQLAlchemy database models
- `backend/app/schemas/` - Pydantic schemas for validation
- `backend/app/services/` - Business logic layer
- `backend/app/core/` - Core utilities (config, security, Redis client)

#### Testing
**Framework**: Custom test scripts (no formal test framework configured)  
**Test Location**: `backend/test_*.py` (root level)  
**Naming Convention**: `test_*.py`  
**Configuration**: Manual test execution

**Run Tests**:
```bash
cd backend
python test_complete_auth.py      # Test authentication flow
python test_cascading_system.py   # Test cascading system
python test_schools_api.py        # Test schools API
```

---

### Keep-Alive Deploy Service

**Location**: `backend/keep-alive-deploy/`  
**Type**: Python microservice for monitoring and keeping backend alive

#### Configuration
**Main Script**: `enhanced_keep_alive.py`  
**Deployment**: Railway/Render compatible  
**Procfile**: Configured for platform deployment

---

## Key Environment Variables

### Frontend
```
VITE_API_URL=http://localhost:8080
VITE_APP_NAME=Rwanda Education Platform
NODE_ENV=development
```

### Backend
```
DATABASE_URL=postgresql://user:password@localhost:5432/rwanda_edu
SECRET_KEY=your-secret-key-min-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=52428800
```

## Technology Stack Summary

**Frontend**:
- Vue 3 with Composition API
- Vite for fast development and optimized builds
- Tailwind CSS for styling
- Pinia for state management
- Socket.io for real-time features
- IndexedDB for offline-first storage
- PWA with Service Workers

**Backend**:
- FastAPI with async/await support
- PostgreSQL 14+ for relational data
- Redis 7+ for caching and pub/sub
- SQLAlchemy 2.0 ORM
- Alembic for database migrations
- JWT authentication with role-based access control
- WebSockets for real-time bidirectional communication
- GZip middleware for compression

**Infrastructure**:
- Docker containerization
- Docker Compose for local development
- Cloudflare Pages for frontend hosting
- Render/Railway for backend deployment
- Supabase for PostgreSQL and file storage
- Upstash for Redis hosting

## User Roles
- **Students** - Access learning materials, join chat rooms, track progress
- **Teachers** - Manage classes, upload resources, moderate content, conduct live sessions
- **DOS Admins** - Director of Studies administrators for school management
- **Super Admins** - Platform-wide administration
- **Class Teachers** - Classroom-specific teaching functions

## Features
- Real-time chat with teacher moderation
- Live video sessions via Jitsi Meet (end-to-end encrypted)
- Resource sharing (documents, videos, images)
- Direct messaging with approval workflow
- Offline-first architecture with sync capabilities
- Multi-language support (Kinyarwanda, English, French)
- Inter-school networking (165 TVET/TSS schools across Rwanda)
- Message reactions and replies
- Incident reporting and emergency features
- Location-based registration (provinces, districts, sectors, cells, villages)
