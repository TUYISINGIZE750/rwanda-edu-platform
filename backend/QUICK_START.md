# TVET Integration - Quick Start Guide

## 🚀 Setup (3 Steps)

### Step 1: Run Migration
```bash
cd backend
alembic upgrade head
```

### Step 2: Seed Schools
```bash
python seed_tvet_schools.py
```

### Step 3: Test Integration
```bash
python test_tvet_integration.py
```

## 📋 Key Changes

### Database
- **schools** table: Added `trades` column (JSON array)
- **users** table: Added `selected_trade` column (String)

### API Endpoints

#### Get Schools by District (with trades)
```http
GET /api/locations/schools/district/Umujyi wa Kigali/Gasabo
```
Response:
```json
[
  {
    "id": 1,
    "name": "IPRC Kigali",
    "type": "TVET",
    "category": "Public",
    "province": "Umujyi wa Kigali",
    "district": "Gasabo",
    "trades": ["Construction", "ICT", "Hospitality"]
  }
]
```

#### Get Trades for a School
```http
GET /api/locations/schools/1/trades
```
Response:
```json
{
  "school_id": 1,
  "school_name": "IPRC Kigali",
  "trades": ["Construction", "ICT", "Hospitality"]
}
```

#### Register Student with Trade
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "student@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "role": "student",
  "school_id": 1,
  "province": "Umujyi wa Kigali",
  "district": "Gasabo",
  "grade": 10,
  "selected_trade": "ICT",
  "locale": "rw"
}
```

## 🎯 Frontend Integration

### Registration Form Flow:

```javascript
// 1. User selects province and district
const province = "Umujyi wa Kigali";
const district = "Gasabo";

// 2. Fetch schools in that district
const response = await fetch(
  `/api/locations/schools/district/${province}/${district}`
);
const schools = await response.json();

// 3. Display schools with their trades
schools.forEach(school => {
  console.log(`${school.name} offers: ${school.trades.join(', ')}`);
});

// 4. User selects school and trade
const selectedSchool = schools[0];
const selectedTrade = "ICT";

// 5. Register with selected trade
await fetch('/api/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: "student@example.com",
    password: "password123",
    full_name: "John Doe",
    role: "student",
    school_id: selectedSchool.id,
    province: province,
    district: district,
    grade: 10,
    selected_trade: selectedTrade,
    locale: "rw"
  })
});
```

## ✅ Validation

The system automatically validates:
- ✓ Selected trade must be offered by the chosen school
- ✓ Returns error with available trades if invalid
- ✓ Teachers don't need to select a trade

## 📊 Testing

Run the test script to verify everything works:
```bash
python test_tvet_integration.py
```

This will:
1. Check schools have trades
2. Test getting trades for a school
3. Test trade validation
4. Show statistics

## 🔧 Optional: Parse Excel File

If you want to use the official Excel data:
```bash
python parse_tvet_excel.py
```

This creates `official_tvet_schools.json` with parsed data.

## 📝 Notes

- `selected_trade` is optional (only for TVET students)
- Teachers don't need to select a trade
- Trades are stored as JSON arrays in the database
- Each school can have multiple trades
- Students select one trade during registration

## 🆘 Troubleshooting

**No schools found?**
→ Run `python seed_tvet_schools.py`

**Migration error?**
→ Run `alembic upgrade head`

**Trade validation failing?**
→ Check that the trade exists in the school's trades list

## 📚 More Info

See `TVET_INTEGRATION_README.md` for detailed documentation.
