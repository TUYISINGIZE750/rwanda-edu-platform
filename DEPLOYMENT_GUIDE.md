# Rwanda Education Platform - Deployment Guide

## Overview
- **Backend**: Render (Python/FastAPI)
- **Frontend**: Cloudflare Pages (Vue.js)
- **Database**: PostgreSQL (Render)
- **GitHub**: TUYISINGIZE750/rwanda-edu-platform

---

## Step 1: GitHub Setup

### 1.1 Create GitHub Repository
```bash
# Initialize git in your project
cd c:\Users\PC\Music\Holidays learning\rwanda-edu-platform
git init
git config user.name "TUYISINGIZE750"
git config user.email "ltuyisingize58@gmail.com"

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Rwanda Education Platform"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/TUYISINGIZE750/rwanda-edu-platform.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Step 2: Backend Deployment (Render)

### 2.1 Prepare Backend

Update `backend/requirements.txt` with gunicorn:
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic==2.5.0
bcrypt==4.1.1
gunicorn==21.2.0
```

### 2.2 Deploy to Render

1. Go to https://render.com
2. Sign up with GitHub (TUYISINGIZE750)
3. Click "New +" → "Web Service"
4. Connect GitHub repository
5. Configure:
   - **Name**: rwanda-edu-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app.main:app`

6. Add Environment Variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `SECRET_KEY`: Generate secure key
   - `ENVIRONMENT`: production
   - `CORS_ORIGINS`: Your frontend URL

7. Click "Create Web Service"

### 2.3 Create PostgreSQL Database on Render

1. Click "New +" → "PostgreSQL"
2. Configure:
   - **Name**: rwanda-edu-db
   - **Database**: rwanda_edu
   - **Plan**: Free
3. Copy connection string to `DATABASE_URL`

---

## Step 3: Frontend Deployment (Cloudflare Pages)

### 3.1 Prepare Frontend

Update `frontend/.env.production`:
```
VITE_API_URL=https://your-backend-url.onrender.com
```

### 3.2 Deploy to Cloudflare Pages

1. Go to https://dash.cloudflare.com
2. Go to "Pages" → "Create a project"
3. Connect GitHub (TUYISINGIZE750)
4. Select `rwanda-edu-platform` repository
5. Configure:
   - **Framework preset**: Vue
   - **Build command**: `npm run build`
   - **Build output directory**: `dist`
   - **Root directory**: `frontend`

6. Add Environment Variables:
   - `VITE_API_URL`: Your Render backend URL

7. Click "Save and Deploy"

---

## Step 4: Environment Variables

### Backend (Render)
```
DATABASE_URL=postgresql://user:password@host:5432/rwanda_edu
SECRET_KEY=your-secret-key-here
ENVIRONMENT=production
CORS_ORIGINS=["https://your-frontend-domain.com"]
```

### Frontend (Cloudflare)
```
VITE_API_URL=https://your-backend-url.onrender.com
```

---

## Step 5: Testing

### Test Backend
```bash
curl https://your-backend-url.onrender.com/api/v1/health
```

### Test Frontend
Visit: `https://your-frontend-domain.com`

---

## Useful Links

- Render: https://render.com
- Cloudflare Pages: https://pages.cloudflare.com
- GitHub: https://github.com/TUYISINGIZE750

Your system is now live! 🚀
