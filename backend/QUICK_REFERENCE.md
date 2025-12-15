# TVET Registration - Quick Reference Card

## 🎯 Auto-Display Logic

```
Province + District  →  AUTO-DISPLAY Schools
School Selected      →  AUTO-DISPLAY Trades  
Trade Selected       →  AUTO-DISPLAY Levels (1-6)
Level Selected       →  Complete Registration
```

## 📡 API Endpoints

```bash
# Step 1: Get Schools (auto-display after location selection)
GET /api/v1/registration/schools/{province}/{district}

# Step 2: Get Trades (auto-display after school selection)
GET /api/v1/registration/trades/{school_id}

# Step 3: Get Levels (auto-display after trade selection)
GET /api/v1/registration/levels

# Step 4: Register
POST /api/v1/auth/register
```

## 💾 Database Fields

**users table:**
- `selected_trade` (String) - Student's chosen trade
- `selected_level` (String) - Student's chosen level

**schools table:**
- `trades` (JSON) - Array of available trades

## 🚀 Setup Commands

```bash
# 1. Run migration
alembic upgrade head

# 2. Seed schools
python seed_tvet_schools.py

# 3. Test
python test_tvet_integration.py
```

## 📝 Registration Request Example

```json
POST /api/v1/auth/register

{
  "email": "student@example.com",
  "password": "password123",
  "full_name": "Jean Claude",
  "role": "student",
  "school_id": 1,
  "province": "Umujyi wa Kigali",
  "district": "Gasabo",
  "selected_trade": "ICT",
  "selected_level": "Level 3",
  "locale": "rw"
}
```

## 🎨 Frontend Pseudo-code

```javascript
// On province + district change
onLocationChange(province, district) {
  schools = fetch(`/registration/schools/${province}/${district}`)
  // AUTO-DISPLAY schools dropdown
}

// On school selection
onSchoolChange(schoolId) {
  trades = fetch(`/registration/trades/${schoolId}`)
  // AUTO-DISPLAY trades dropdown
}

// On trade selection
onTradeChange(trade) {
  levels = fetch(`/registration/levels`)
  // AUTO-DISPLAY levels dropdown (Level 1-6)
}

// On submit
onSubmit() {
  register({
    school_id, 
    selected_trade, 
    selected_level,
    ...otherFields
  })
}
```

## ✅ Available Levels

- Level 1
- Level 2
- Level 3
- Level 4
- Level 5
- Level 6

## 📚 Documentation Files

- `REGISTRATION_FLOW_GUIDE.md` - Complete implementation guide
- `IMPLEMENTATION_SUMMARY.md` - Technical details
- `TVET_INTEGRATION_README.md` - Full documentation
- `QUICK_START.md` - Quick setup guide

## 🔗 Key Features

✅ Cascading dropdowns (auto-display)
✅ Trade validation
✅ Level selection (1-6)
✅ Clean API design
✅ Frontend-ready endpoints
