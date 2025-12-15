# Kamonyi District Learning Hub Platform

## 🎓 Overview
Modern learning platform for schools in Kamonyi District, Rwanda. Safe, moderated communication with role-based access control.

## 🏫 Schools in Kamonyi District

### 1. GS Kamonyi (School ID: 1)
- **Sector:** Kamonyi
- **Users:** 56 (1 admin, 5 teachers, 50 students)
- **Grades:** S1-S5 (10 students per grade)

### 2. GS Runda (School ID: 2)
- **Sector:** Runda
- **Users:** 56 (1 admin, 5 teachers, 50 students)
- **Grades:** S1-S5 (10 students per grade)

**Total Users:** 112 (2 admins, 10 teachers, 100 students)

---

## 🔐 Login Credentials

### GS Kamonyi (School 1)

**Admin:**
- Email: `admin@school1.rw`
- Password: `admin123`
- Role: Select "👨💼 Admin"

**Teachers:**
- Email: `teacher1@school1.rw` to `teacher5@school1.rw`
- Password: `teacher123`
- Role: Select "👨🏫 Teacher"

**Students:**
- Email: `student11@school1.rw` to `student510@school1.rw`
- Password: `student123`
- Role: Select "👨🎓 Student"
- Format: `student{grade}{number}@school1.rw`

### GS Runda (School 2)

**Admin:**
- Email: `admin@school2.rw`
- Password: `admin123`
- Role: Select "👨💼 Admin"

**Teachers:**
- Email: `teacher1@school2.rw` to `teacher5@school2.rw`
- Password: `teacher123`
- Role: Select "👨🏫 Teacher"

**Students:**
- Email: `student11@school2.rw` to `student510@school2.rw`
- Password: `student123`
- Role: Select "👨🎓 Student"

---

## 🌐 Access Platform

**Landing Page:** http://localhost:5174

### New Features:
1. **Role Selection on Login** - Users must select their role (Admin/Teacher/Student) before logging in
2. **Role Verification** - System verifies the selected role matches the account
3. **Kamonyi Branding** - Updated to "Kamonyi Learning Hub"
4. **2 Schools Only** - GS Kamonyi and GS Runda

---

## 📋 How to Login

1. Open http://localhost:5174
2. Click "Login"
3. **Select your role** from dropdown:
   - 👨💼 Admin
   - 👨🏫 Teacher
   - 👨🎓 Student
4. Enter your email
5. Enter your password
6. Click "Login"

**Note:** If your role doesn't match your account, you'll get an error message.

---

## 📝 How to Register

1. Open http://localhost:5174
2. Click "Register"
3. Fill in:
   - Full Name
   - Email
   - Password
   - **Role** (Student/Teacher)
   - **School** (GS Kamonyi or GS Runda)
   - **Grade** (if student: S1-S5)
   - Language (Kinyarwanda/English/French)
4. Click "Register"
5. Auto-login after successful registration

---

## 🎯 Features by Role

### 👨💼 Admin
- System dashboard
- User management
- School analytics
- Engagement reports
- Full oversight

### 👨🏫 Teacher
- Auto-approved messaging
- Content moderation
- DM request approval
- Resource uploads
- Incident resolution

### 👨🎓 Student
- Moderated messaging
- DM requests
- Resource downloads
- Content flagging
- Grade-specific access

---

## 📊 Database Structure

### Users: 112 Total
- **Admins:** 2 (1 per school)
- **Teachers:** 10 (5 per school)
- **Students:** 100 (50 per school)

### Groups: 16 Total
- **Classes:** 10 (5 per school: S1-S5)
- **Clubs:** 6 (3 per school)

### Channels: 64 Total
- **Per Group:** 4 channels
- **Types:** Announcements, Discussion, Resources, Office Hours

---

## 🚀 Quick Test

### Test Admin Features (GS Kamonyi)
```
1. Login as admin@school1.rw / admin123
2. Select "👨💼 Admin" role
3. View dashboard
4. Manage users
5. Check analytics
```

### Test Teacher Features (GS Kamonyi)
```
1. Login as teacher1@school1.rw / teacher123
2. Select "👨🏫 Teacher" role
3. Post announcement
4. Moderate messages
5. Approve DM requests
```

### Test Student Features (GS Kamonyi)
```
1. Login as student11@school1.rw / student123
2. Select "👨🎓 Student" role
3. Post message (pending approval)
4. Request DM with teacher
5. Download resources
```

---

## 🎨 Modern Design Features

### Landing Page
- ✅ Modern hero section
- ✅ Kamonyi District branding
- ✅ School showcase with sectors
- ✅ Feature highlights
- ✅ Quick login modal
- ✅ Registration form

### Login System
- ✅ Role selection dropdown
- ✅ Role verification
- ✅ Error handling
- ✅ Modern UI design
- ✅ Responsive layout

### Registration System
- ✅ Full form with validation
- ✅ School selection (2 schools)
- ✅ Grade selection (for students)
- ✅ Language preference
- ✅ Auto-login after registration

---

## 📈 Statistics

- **2 Schools** in Kamonyi District
- **112 Users** across both schools
- **16 Groups** (classes and clubs)
- **64 Channels** for communication
- **3 Languages** supported
- **100% Moderated** content

---

## 🔧 Technical Details

### Backend
- FastAPI with role-based access
- PostgreSQL database
- Redis caching
- JWT authentication

### Frontend
- Vue 3 with modern design
- Role selection on login
- Responsive UI
- PWA support

### Security
- Role verification
- School-based isolation
- Content moderation
- Time-limited DM windows

---

## 📞 Support

**Platform URL:** http://localhost:5174
**API Docs:** http://localhost:8080/docs
**Health Check:** http://localhost:8080/health

---

**✅ Platform Status:** Fully Operational
**🏫 District:** Kamonyi, Rwanda
**📅 Last Updated:** December 2024
