# Rwanda TVET Schools Integration

## Quick Start

### Automated Setup
```bash
setup-tvet.bat
```

This will:
1. Run database migrations
2. Seed 40 TVET/TSS schools
3. Verify installation

### Manual Setup
```bash
# 1. Migrate database
cd backend
python -m alembic upgrade head

# 2. Seed schools
python seed_tvet_schools.py

# 3. Start services
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## What's Included

### 40 Real TVET/TSS Schools
- **5 IPRC** (Integrated Polytechnic Regional Centres)
  - IPRC Kigali (Kimironko, Gasabo)
  - IPRC Huye (Ngoma, Huye)
  - IPRC Musanze (Muhoza, Musanze)
  - IPRC Ngoma (Kibungo, Ngoma)
  - IPRC Karongi (Bwishyura, Karongi)

- **15 TSS** (Technical Secondary Schools)
  - TSS Byimana, TSS Murunda, TSS Rubengera, etc.

- **20 CFP & Other TVET** (Vocational Training Centers)
  - Don Bosco VTC schools
  - Tumba College of Technology
  - Various district-level TVET centers

### Location Hierarchy
```
Province (5 total)
  └── District (30 total)
      └── Sector (416 total)
          └── TVET/TSS Schools (40 mapped)
```

### Available Trades/Programs
- **Construction**: Masonry, Carpentry, Plumbing, Electrical Installation
- **Automotive**: Mechanics, Automotive Technology
- **ICT**: Information Technology, Computer Science
- **Hospitality**: Culinary Arts, Hotel Management, Tourism
- **Agriculture**: Crop Production, Animal Husbandry
- **Manufacturing**: Welding, Electronics, Metalwork
- **Services**: Tailoring, Hairdressing, Business Management

## Registration Flow

### For Students
1. Visit `/register`
2. Enter full name and email
3. Create password
4. Select role: **Student**
5. **Select Location:**
   - Province (e.g., "Umujyi wa Kigali")
   - District (e.g., "Gasabo")
   - Sector (e.g., "Kimironko")
6. **Select School:** View TVET/TSS schools in your sector
7. Select grade (Year 1, 2, or 3)
8. Choose language (Kinyarwanda, English, French)
9. Register

### For Teachers
Same flow as students, but:
- Select role: **Teacher**
- No grade selection required
- Can access moderation features

## API Examples

### Get Provinces
```bash
GET /api/v1/api/locations/provinces
```
Response:
```json
[
  {"name": "Umujyi wa Kigali"},
  {"name": "Amajyepfo"},
  {"name": "Iburasirazuba"},
  {"name": "Iburengerazuba"},
  {"name": "Amajyaruguru"}
]
```

### Get Districts
```bash
GET /api/v1/api/locations/districts/Umujyi wa Kigali
```
Response:
```json
[
  {"name": "Gasabo"},
  {"name": "Kicukiro"},
  {"name": "Nyarugenge"}
]
```

### Get Schools in Sector
```bash
GET /api/v1/api/locations/schools/sector/Umujyi wa Kigali/Gasabo/Kimironko
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
    "sector": "Kimironko",
    "trades": ["Construction", "Electrical Installation", "Plumbing", "Automotive", "ICT", "Hospitality"]
  }
]
```

## Database Schema

### Schools Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | School name |
| type | String | TVET or TSS |
| category | String | Public/Private/Faith-Based |
| province | String | Province name |
| district | String | District name |
| sector | String | Sector name |
| trades | JSON | Array of programs |

### Users Table (New Fields)
| Column | Type | Description |
|--------|------|-------------|
| province | String | User's province |
| district | String | User's district |
| sector | String | User's sector |

## Files Created/Modified

### Backend
- ✅ `backend/tvet_schools_data.py` - 40 schools database
- ✅ `backend/seed_tvet_schools.py` - Seeding script
- ✅ `backend/app/models/school.py` - School model
- ✅ `backend/app/models/user.py` - Updated with location fields
- ✅ `backend/app/services/location_service.py` - Location queries
- ✅ `backend/app/api/locations.py` - Location endpoints
- ✅ `backend/app/api/auth.py` - Updated registration
- ✅ `backend/app/schemas/user.py` - Updated schemas
- ✅ `backend/alembic/versions/add_location_and_schools.py` - Migration

### Frontend
- ✅ `frontend/src/views/RegisterView.vue` - Registration form
- ✅ `frontend/src/views/LoginView.vue` - Added register link
- ✅ `frontend/src/router/index.js` - Added register route
- ✅ `frontend/src/locales/en.json` - English translations
- ✅ `frontend/src/locales/fr.json` - French translations
- ✅ `frontend/src/locales/rw.json` - Kinyarwanda translations

### Documentation
- ✅ `TVET_SETUP_GUIDE.md` - Comprehensive guide
- ✅ `TVET_README.md` - Quick reference
- ✅ `setup-tvet.bat` - Automated setup

## School Distribution by Province

| Province | TVET | TSS | Total |
|----------|------|-----|-------|
| Kigali City | 5 | 0 | 5 |
| Southern | 4 | 5 | 9 |
| Eastern | 3 | 3 | 6 |
| Western | 4 | 4 | 8 |
| Northern | 3 | 3 | 6 |
| **Total** | **19** | **15** | **34** |

## Key Features

### 1. Real Data
- Actual TVET/TSS schools from REB/WDA
- Real Rwanda administrative boundaries
- Accurate sector-level mapping

### 2. Smart Filtering
- Cascading dropdowns
- Schools filtered by selected sector
- No irrelevant options shown

### 3. Multilingual
- Full Kinyarwanda support
- English and French translations
- Language-specific UI

### 4. User-Friendly
- Clear step-by-step process
- Helpful error messages
- Responsive design

### 5. Scalable
- Easy to add more schools
- Simple location updates
- Extensible architecture

## Testing Checklist

- [ ] Run `setup-tvet.bat`
- [ ] Verify 40 schools in database
- [ ] Start backend and frontend
- [ ] Visit `/register`
- [ ] Test province dropdown
- [ ] Test district filtering
- [ ] Test sector filtering
- [ ] Verify schools appear
- [ ] Complete registration
- [ ] Login with new account
- [ ] Verify location data saved

## Common Issues

### No schools in sector?
Some sectors don't have TVET/TSS schools. Try:
- Selecting a different sector
- Checking nearby sectors
- Verifying school was seeded correctly

### Dropdown not loading?
- Check backend is running
- Verify `locations.json` exists
- Check browser console for errors
- Verify API endpoints work

### Registration fails?
- Ensure all fields filled
- Check password length (min 6)
- Verify school selected
- Check backend logs

## Next Steps

1. **Run Setup**: `setup-tvet.bat`
2. **Start Services**: Backend + Frontend
3. **Test Registration**: Create student/teacher account
4. **Explore Platform**: Login and use features

## Support

- 📖 Full Guide: `TVET_SETUP_GUIDE.md`
- 🔧 API Docs: `http://localhost:8000/docs`
- 📊 Database: Check with SQL client
- 🐛 Logs: `backend/logs/`

---

**Built for Rwanda's TVET Education System** 🇷🇼
