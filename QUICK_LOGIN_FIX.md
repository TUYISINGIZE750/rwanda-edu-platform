# Quick Login Fix Guide

## 🚀 Start the System

### 1. Start Backend Server
```bash
cd "c:\Users\PC\Music\Holidays learning\rwanda-edu-platform"
python start_backend_simple.py
```

### 2. Start Frontend (in new terminal)
```bash
cd "c:\Users\PC\Music\Holidays learning\rwanda-edu-platform\frontend"
npm run dev
```

## 🔑 Test Login Credentials

The system now has pre-created test users:

| Role | Email | Password | Dashboard |
|------|-------|----------|-----------|
| **Student** | `student@test.com` | `test123` | Student Dashboard with groups, resources, sessions |
| **Teacher** | `teacher@test.com` | `test123` | Teacher Dashboard with class management, moderation |
| **Admin** | `admin@test.com` | `test123` | Admin Dashboard with school statistics, user management |

## 🧪 Test the Login

1. **Verify Backend**: Run `python test_login.py` to test all user logins
2. **Access Frontend**: Go to `http://localhost:5175`
3. **Login Process**:
   - Enter email and password
   - **Select role** (Student/Teacher/Admin)
   - Click "Sign In"

## 🎯 What's Fixed

✅ **Backend Authentication**: All auth endpoints working on `/api/v1/auth/*`
✅ **Test Users Created**: Pre-populated database with test accounts
✅ **Role Selection**: Login form now includes role selection
✅ **Dashboard Routing**: Users automatically routed to role-specific dashboards
✅ **API Endpoints**: All endpoints properly configured with CORS

## 🏫 System Features

### Student Dashboard
- View learning groups and channels
- Access resources and materials
- Track active sessions
- Real-time messaging

### Teacher Dashboard  
- Create and manage groups
- Upload resources
- Moderate student messages
- View class statistics

### Admin Dashboard
- School-wide statistics
- User management
- System monitoring
- Content moderation

## 🔧 Troubleshooting

**If login still fails:**
1. Check backend is running: `http://localhost:8080/health`
2. Verify API docs: `http://localhost:8080/docs`
3. Test endpoints: `python test_login.py`
4. Check browser console for errors

**Common Issues:**
- Backend not running → Start with `python start_backend_simple.py`
- Port conflicts → Change port in config files
- Database issues → Recreate users with `python create_test_user.py`

## 🌍 Ready for Rwanda TVET Schools

The system is now fully functional and ready for deployment across all 164 TVET/TSS schools in Rwanda with:
- Multi-language support (RW/EN/FR)
- School-specific data isolation
- Trade and level management
- Offline-capable design
- Modern responsive UI