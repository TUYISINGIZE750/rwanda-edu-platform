## Manual Testing Guide - Student & Teacher Registration/Login

### Quick Start (Automated)

**Option 1: Run Everything Automatically**
```bash
START_SYSTEM.bat
```
This will:
- Setup database
- Start backend (port 8080)
- Start frontend (port 5173)
- Run authentication tests

---

### Manual Testing Steps

#### Step 1: Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```
Backend runs on: http://localhost:8080
API Docs: http://localhost:8080/docs

#### Step 2: Start Frontend (in new terminal)
```bash
cd frontend
npm run dev
```
Frontend runs on: http://localhost:5173

#### Step 3: Test with Browser

**Test Student Registration:**
1. Open http://localhost:5173/register
2. Fill form:
   - Select Province: "Umujyi wa Kigali"
   - Select District: "Gasabo"
   - **Schools auto-display** ✓
   - Select a school
   - **Trades auto-display** ✓
   - Select a trade
   - **Levels auto-display** (Level 1-6) ✓
   - Select a level
   - Fill email, password, name
   - Role: Student
   - Submit

**Test Teacher Registration:**
1. Open http://localhost:5173/register
2. Fill form:
   - Select Province: "Umujyi wa Kigali"
   - Select District: "Gasabo"
   - **Schools auto-display** ✓
   - Select a school
   - Fill email, password, name
   - Role: Teacher
   - Submit (no trade/level needed)

**Test Login:**
1. Open http://localhost:5173/login
2. Enter email and password
3. Click Login
4. Should redirect to dashboard

---

### API Testing (Using curl or Postman)

#### Test 1: Get Schools
```bash
curl "http://localhost:8080/api/v1/registration/schools/Umujyi%20wa%20Kigali/Gasabo"
```

#### Test 2: Get Trades for School ID 1
```bash
curl "http://localhost:8080/api/v1/registration/trades/1"
```

#### Test 3: Get Levels
```bash
curl "http://localhost:8080/api/v1/registration/levels"
```

#### Test 4: Register Student
```bash
curl -X POST "http://localhost:8080/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"student@test.com\",
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

#### Test 5: Register Teacher
```bash
curl -X POST "http://localhost:8080/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"teacher@test.com\",
    \"password\": \"Test123!\",
    \"full_name\": \"Test Teacher\",
    \"role\": \"teacher\",
    \"school_id\": 1,
    \"province\": \"Umujyi wa Kigali\",
    \"district\": \"Gasabo\",
    \"locale\": \"rw\"
  }"
```

#### Test 6: Login
```bash
curl -X POST "http://localhost:8080/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"student@test.com\",
    \"password\": \"Test123!\"
  }"
```

---

### Automated Testing

**Run Python Test Script:**
```bash
cd backend
python test_auth_endpoints.py
```

This tests:
- ✓ Student registration with TVET flow
- ✓ Teacher registration
- ✓ Login for both roles

---

### Expected Results

**✅ Student Registration Flow:**
1. Select Province + District → Schools appear
2. Select School → Trades appear
3. Select Trade → Levels appear (Level 1-6)
4. Submit → Success message

**✅ Teacher Registration Flow:**
1. Select Province + District → Schools appear
2. Select School → Ready to submit
3. Submit → Success message (no trade/level needed)

**✅ Login:**
- Returns JWT token
- Returns user info
- Redirects to dashboard

---

### Troubleshooting

**Backend not starting?**
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
python seed_tvet_schools.py
```

**Frontend not starting?**
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

**Database errors?**
```bash
cd backend
alembic downgrade base
alembic upgrade head
python seed_tvet_schools.py
```

---

### Quick Verification

**Check if backend is running:**
```bash
curl http://localhost:8080/health
```
Should return: `{"status":"healthy"}`

**Check if schools exist:**
```bash
curl "http://localhost:8080/api/v1/registration/schools/Umujyi%20wa%20Kigali/Gasabo"
```
Should return list of schools

**Check API documentation:**
Open: http://localhost:8080/docs
