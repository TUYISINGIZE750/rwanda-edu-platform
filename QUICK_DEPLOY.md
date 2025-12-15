# Quick Deployment Steps

## 1. GitHub Setup (5 minutes)

```bash
cd "c:\Users\PC\Music\Holidays learning\rwanda-edu-platform"
git init
git config user.name "TUYISINGIZE750"
git config user.email "ltuyisingize58@gmail.com"
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/TUYISINGIZE750/rwanda-edu-platform.git
git branch -M main
git push -u origin main
```

## 2. Render Backend Deployment (10 minutes)

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Select `rwanda-edu-platform` repository
5. Fill in:
   - **Name**: rwanda-edu-backend
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app.main:app`
6. Add Environment Variables:
   ```
   DATABASE_URL=postgresql://user:password@host:5432/rwanda_edu
   SECRET_KEY=generate-a-random-secret-key
   ENVIRONMENT=production
   CORS_ORIGINS=["https://your-cloudflare-domain.com"]
   ```
7. Click "Create Web Service"
8. Wait for deployment (2-3 minutes)
9. Copy the backend URL (e.g., https://rwanda-edu-backend.onrender.com)

## 3. Render PostgreSQL Database (5 minutes)

1. In Render dashboard, click "New +" → "PostgreSQL"
2. Fill in:
   - **Name**: rwanda-edu-db
   - **Database**: rwanda_edu
   - **Plan**: Free
3. Copy the connection string
4. Update backend's `DATABASE_URL` environment variable

## 4. Cloudflare Frontend Deployment (10 minutes)

1. Go to https://dash.cloudflare.com
2. Sign up or login
3. Go to "Pages" → "Create a project"
4. Select "Connect to Git"
5. Authorize GitHub and select `rwanda-edu-platform`
6. Fill in:
   - **Framework preset**: Vue
   - **Build command**: `npm run build`
   - **Build output directory**: `dist`
   - **Root directory**: `frontend`
7. Add Environment Variable:
   ```
   VITE_API_URL=https://rwanda-edu-backend.onrender.com
   ```
8. Click "Save and Deploy"
9. Wait for deployment (2-3 minutes)
10. Copy the frontend URL (e.g., https://rwanda-edu-platform.pages.dev)

## 5. Update Backend CORS (2 minutes)

1. Go back to Render backend service
2. Update `CORS_ORIGINS` with your Cloudflare URL:
   ```
   CORS_ORIGINS=["https://rwanda-edu-platform.pages.dev"]
   ```
3. Service will auto-redeploy

## 6. Test Your System (5 minutes)

1. Visit: https://rwanda-edu-platform.pages.dev
2. Try to login
3. Check browser console for errors
4. If issues, check Render logs: Dashboard → Service → Logs

## 7. Custom Domain (Optional)

### For Backend (Render)
1. Render Dashboard → Service → Settings
2. Add custom domain
3. Update DNS records

### For Frontend (Cloudflare)
1. Cloudflare Pages → Project → Custom domains
2. Add your domain
3. Follow DNS setup

---

## Troubleshooting

**Blank page on frontend?**
- Check browser console (F12)
- Verify VITE_API_URL is correct
- Check Cloudflare build logs

**API errors?**
- Check Render backend logs
- Verify DATABASE_URL is correct
- Check CORS_ORIGINS setting

**Database connection failed?**
- Verify PostgreSQL is running on Render
- Check DATABASE_URL format
- Ensure credentials are correct

---

## Your Live URLs

- **Frontend**: https://rwanda-edu-platform.pages.dev
- **Backend**: https://rwanda-edu-backend.onrender.com
- **GitHub**: https://github.com/TUYISINGIZE750/rwanda-edu-platform

🚀 Your system is now live!
