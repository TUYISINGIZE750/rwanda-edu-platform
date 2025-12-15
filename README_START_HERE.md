# 🚀 START HERE - TVET Registration System

## Quick Start (One Command)

```bash
START_SYSTEM.bat
```

This will:
1. ✅ Setup database
2. ✅ Seed TVET schools
3. ✅ Start backend on **http://localhost:8080**
4. ✅ Start frontend on **http://localhost:5173**
5. ✅ Run authentication tests

---

## System URLs

- **Backend API:** http://localhost:8080
- **API Documentation:** http://localhost:8080/docs
- **Frontend:** http://localhost:5173
- **Health Check:** http://localhost:8080/health

---

## What's Working

### ✅ Student Registration Flow
```
1. Select Province + District
   → System AUTO-DISPLAYS TVET/TSS schools

2. Select School
   → System AUTO-DISPLAYS trades for that school

3. Select Trade
   → System AUTO-DISPLAYS levels (Level 1-6)

4. Select Level + Submit
   → Registration complete!
```

### ✅ Teacher Registration Flow
```
1. Select Province + District
   → System AUTO-DISPLAYS schools

2. Select School + Submit
   → Registration complete! (no trade/level needed)
```

### ✅ Login
- Works for both students and teachers
- Returns JWT token
- Redirects to dashboard

---

## API Endpoints (Port 8080)

```bash
# Get schools by district
GET http://localhost:8080/api/v1/registration/schools/{province}/{district}

# Get trades for school
GET http://localhost:8080/api/v1/registration/trades/{school_id}

# Get levels
GET http://localhost:8080/api/v1/registration/levels

# Register
POST http://localhost:8080/api/v1/auth/register

# Login
POST http://localhost:8080/api/v1/auth/login
```

---

## Test Registration

### Test Student (with curl)
```bash
curl -X POST "http://localhost:8080/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"student@test.rw\",
    \"password\": \"Test123!\",
    \"full_name\": \"Test Student\",
    \"role\": \"student\",
    \"school_id\": 1,
    \"province\": \"Umujyi wa Kigali\",
    \"district\": \"Gasabo\",
    \"selected_trade\": \"ICT\",
    \"selected_level\": \"Level 3\",
    \"locale\": \"rw\"
  }"
```

### Test Teacher (with curl)
```bash
curl -X POST "http://localhost:8080/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"teacher@test.rw\",
    \"password\": \"Test123!\",
    \"full_name\": \"Test Teacher\",
    \"role\": \"teacher\",
    \"school_id\": 1,
    \"province\": \"Umujyi wa Kigali\",
    \"district\": \"Gasabo\",
    \"locale\": \"rw\"
  }"
```

---

## Manual Testing

1. **Start System:**
   ```bash
   START_SYSTEM.bat
   ```

2. **Open Frontend:**
   - Go to http://localhost:5173
   - Click "Register"
   - Follow the cascading form

3. **Test API:**
   - Go to http://localhost:8080/docs
   - Try the endpoints interactively

---

## Troubleshooting

**Backend won't start?**
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
python seed_tvet_schools.py
```

**Frontend won't start?**
```bash
cd frontend
npm install
npm run dev
```

**No schools appearing?**
```bash
cd backend
python seed_tvet_schools.py
```

---

## Files & Documentation

- `START_SYSTEM.bat` - Start everything
- `FINAL_VERIFICATION.md` - Complete verification checklist
- `MANUAL_TEST_GUIDE.md` - Detailed testing guide
- `REGISTRATION_FLOW_GUIDE.md` - Implementation guide
- `QUICK_REFERENCE.md` - API quick reference

---

## ✅ System Status

- ✅ Database schema with trades & levels
- ✅ Auto-cascading registration flow
- ✅ Student registration (Province → District → Schools → Trades → Levels)
- ✅ Teacher registration (Province → District → Schools)
- ✅ Login for both roles
- ✅ JWT authentication
- ✅ API endpoints on port **8080**
- ✅ Frontend on port **5173**

**Everything is ready to use! 🎉**
