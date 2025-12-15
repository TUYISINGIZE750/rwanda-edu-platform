# 🎯 Quick Reference - Official TVET System

## Setup (30 seconds)
```bash
setup-official-tvet.bat
```

## Start Services
```bash
# Terminal 1
cd backend && uvicorn app.main:app --reload

# Terminal 2
cd frontend && npm run dev
```

## Registration URL
```
http://localhost:5173/register
```

## System Overview

### 70 Official Schools
| Province | Schools | Districts |
|----------|---------|-----------|
| Kigali City | 10 | 3 |
| Southern | 18 | 8 |
| Eastern | 14 | 7 |
| Western | 16 | 7 |
| Northern | 10 | 5 |

### Registration Flow
```
1. Personal Info → 2. Province → 3. District → 4. School → 5. Done
```

### School Types
- **TVET** (45): Vocational training centers
- **TSS** (25): Technical secondary schools

## API Endpoints

```bash
# Provinces
GET /api/v1/api/locations/provinces

# Districts
GET /api/v1/api/locations/districts/{province}

# Schools
GET /api/v1/api/locations/schools/district/{province}/{district}

# Register
POST /api/v1/auth/register
```

## Example Districts with Schools

### Kigali City
- **Gasabo** (5): IPRC Kigali, TCT, ETOILE, Don Bosco, Akilah
- **Kicukiro** (3): ETO, Don Bosco Gatenga, CFP
- **Nyarugenge** (2): ETS Kigali, CFP

### Southern Province
- **Huye** (4): IPRC Huye, ETS Murambi, GS Saint Kizito, CFP
- **Ruhango** (2): TSS Byimana, CFP
- **Kamonyi** (2): ETS Kamonyi, CFP

### Eastern Province
- **Ngoma** (2): IPRC Ngoma, ETS Kibungo
- **Rwamagana** (3): TSS Murunda, Don Bosco Muhazi, CFP

### Western Province
- **Karongi** (3): IPRC Karongi, TSS Rubengera, CFP
- **Rubavu** (3): ETS Rubavu, CFP Gisenyi, Don Bosco

### Northern Province
- **Musanze** (3): IPRC Musanze, ETS Musanze, CFP
- **Gicumbi** (2): ETS Gicumbi, CFP Byumba

## Database Check

```bash
# Total schools
python -c "from app.core.database import SessionLocal; from app.models.school import School; db = SessionLocal(); print(db.query(School).count()); db.close()"

# Schools by province
python -c "from app.core.database import SessionLocal; from app.models.school import School; db = SessionLocal(); [print(f'{p[0]}: {db.query(School).filter(School.province==p[0]).count()}') for p in db.query(School.province).distinct().all()]; db.close()"
```

## User Data Structure

```python
{
  "email": "student@example.com",
  "full_name": "Jean Doe",
  "role": "student",  # or "teacher"
  "school_id": 1,  # IPRC Kigali
  "province": "Kigali City",
  "district": "Gasabo",
  "grade": 2,  # For students only
  "locale": "rw"  # rw, en, or fr
}
```

## Common Tasks

### Add New School
1. Edit `backend/official_tvet_schools.py`
2. Add entry with id, name, district, province, type, category
3. Run `python seed_official_schools.py`

### Test Registration
1. Visit `/register`
2. Fill form
3. Select "Kigali City" → "Gasabo"
4. Choose "IPRC Kigali"
5. Complete and register

### Query Schools
```python
from app.core.database import SessionLocal
from app.models.school import School

db = SessionLocal()

# Get all schools in Gasabo
schools = db.query(School).filter(
    School.province == "Kigali City",
    School.district == "Gasabo"
).all()

for school in schools:
    print(f"{school.name} ({school.type})")

db.close()
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No schools showing | Run seed script |
| Districts not loading | Check backend running |
| Registration fails | Verify all fields filled |
| School not in list | Check district selection |

## File Locations

```
backend/
├── official_tvet_schools.py      # 70 schools data
├── seed_official_schools.py      # Seeding script
└── app/
    ├── models/school.py          # School model
    ├── api/locations.py          # Location endpoints
    └── services/location_service.py

frontend/
└── src/
    ├── views/RegisterView.vue    # Registration form
    └── locales/                  # Translations
```

## Support

- **Docs**: `OFFICIAL_TVET_GUIDE.md`
- **API**: `http://localhost:8000/docs`
- **Logs**: `backend/logs/`

---

**70 Schools | 3-Step Registration | Province → District → School** 🎓
