# Official TVET Schools - Implementation Guide

## Overview
This system uses **70 official TVET/TSS schools** from Rwanda, organized by **Province → District** structure for simplified registration.

## Quick Setup

```bash
setup-official-tvet.bat
```

## Registration Flow

### Simplified Process
1. **Select Province** (5 options)
2. **Select District** (filtered by province)
3. **Select School** (all TVET/TSS schools in that district)
4. Complete registration

**No sector selection needed** - schools are shown directly at district level.

## School Distribution

### Total: 70 Schools

#### Kigali City (10 schools)
- **Gasabo**: 5 schools (IPRC Kigali, TCT, ETOILE, Don Bosco, Akilah)
- **Kicukiro**: 3 schools (ETO Kicukiro, Don Bosco Gatenga, CFP)
- **Nyarugenge**: 2 schools (ETS Kigali, CFP Nyarugenge)

#### Southern Province (18 schools)
- **Huye**: 4 schools (IPRC Huye, ETS Murambi, GS Saint Kizito, CFP)
- **Nyanza**: 2 schools
- **Muhanga**: 2 schools
- **Ruhango**: 2 schools (TSS Byimana, CFP)
- **Kamonyi**: 2 schools
- **Gisagara**: 2 schools
- **Nyaruguru**: 2 schools
- **Nyamagabe**: 2 schools

#### Eastern Province (14 schools)
- **Ngoma**: 2 schools (IPRC Ngoma, ETS Kibungo)
- **Rwamagana**: 3 schools (TSS Murunda, Don Bosco Muhazi, CFP)
- **Kayonza**: 2 schools
- **Kirehe**: 2 schools
- **Nyagatare**: 2 schools
- **Gatsibo**: 2 schools
- **Bugesera**: 2 schools

#### Western Province (16 schools)
- **Karongi**: 3 schools (IPRC Karongi, TSS Rubengera, CFP)
- **Rubavu**: 3 schools (ETS Rubavu, CFP Gisenyi, Don Bosco)
- **Rusizi**: 2 schools
- **Nyamasheke**: 2 schools
- **Rutsiro**: 2 schools
- **Ngororero**: 2 schools
- **Nyabihu**: 2 schools

#### Northern Province (10 schools)
- **Musanze**: 3 schools (IPRC Musanze, ETS Musanze, CFP)
- **Burera**: 2 schools
- **Gicumbi**: 2 schools
- **Gakenke**: 2 schools
- **Rulindo**: 2 schools

## API Endpoints

### Get Provinces
```
GET /api/v1/api/locations/provinces
```

### Get Districts
```
GET /api/v1/api/locations/districts/{province}
```

### Get Schools by District
```
GET /api/v1/api/locations/schools/district/{province}/{district}
```

## Example Usage

### 1. Student Registration in Kigali
```
1. Select Province: "Kigali City"
2. Select District: "Gasabo"
3. See 5 schools:
   - IPRC Kigali (TVET - Public)
   - Tumba College of Technology (TVET - Public)
   - ETOILE (TSS - Public)
   - Don Bosco TVET Kigali (TVET - Faith-Based)
   - Akilah Institute for Women (TVET - Private)
4. Select school and complete registration
```

### 2. Student Registration in Huye
```
1. Select Province: "Southern Province"
2. Select District: "Huye"
3. See 4 schools:
   - IPRC Huye (TVET - Public)
   - ETS Murambi (TSS - Public)
   - GS Saint Kizito (TSS - Faith-Based)
   - CFP Huye (TVET - Public)
4. Select school and complete registration
```

## Database Schema

### Schools Table
```sql
CREATE TABLE schools (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    type VARCHAR NOT NULL,  -- 'TVET' or 'TSS'
    category VARCHAR NOT NULL,  -- 'Public', 'Private', 'Faith-Based'
    province VARCHAR NOT NULL,
    district VARCHAR NOT NULL
);
```

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    full_name VARCHAR NOT NULL,
    role VARCHAR NOT NULL,  -- 'student' or 'teacher'
    school_id INTEGER NOT NULL,
    province VARCHAR NOT NULL,
    district VARCHAR NOT NULL,
    grade INTEGER,  -- For students only
    locale VARCHAR DEFAULT 'rw'
);
```

## Key Features

### 1. Official Schools Only
All 70 schools are officially accredited TVET/TSS institutions recognized by REB/WDA.

### 2. Simplified Selection
- No sector selection needed
- Direct Province → District → School flow
- Faster registration process

### 3. Complete Coverage
- All 5 provinces covered
- All 30 districts with TVET schools included
- Mix of Public, Private, and Faith-Based institutions

### 4. School Types
- **TVET**: Vocational training centers (CFP, IPRC, Don Bosco)
- **TSS**: Technical secondary schools (ETS, TSS)

## Testing

### Test Registration
1. Start services: `setup-official-tvet.bat`
2. Visit: `http://localhost:5173/register`
3. Select "Kigali City" → "Gasabo"
4. Should see 5 schools
5. Complete registration

### Verify Data
```bash
# Check total schools
python -c "from app.core.database import SessionLocal; from app.models.school import School; db = SessionLocal(); print(f'Total: {db.query(School).count()}'); db.close()"

# Check schools by district
python -c "from app.core.database import SessionLocal; from app.models.school import School; db = SessionLocal(); schools = db.query(School).filter(School.district=='Gasabo').all(); [print(f'{s.name} ({s.type})') for s in schools]; db.close()"
```

## Benefits

### For Students
- Easy school discovery
- See all schools in their district
- Clear school types and categories
- Fast registration

### For System
- Accurate official data
- Simplified data structure
- Better performance (no sector queries)
- Easier maintenance

## Files Modified

### Backend
- `official_tvet_schools.py` - 70 schools database
- `seed_official_schools.py` - Seeding script
- `app/models/school.py` - Removed sector field
- `app/models/user.py` - Removed sector field
- `app/services/location_service.py` - Simplified queries
- `app/api/locations.py` - Updated endpoints
- `app/schemas/user.py` - Updated schema
- `app/api/auth.py` - Updated registration

### Frontend
- `views/RegisterView.vue` - Simplified to 2-step location selection
- `locales/*.json` - Updated translations

### Database
- `alembic/versions/update_to_district_only.py` - Migration

## Maintenance

### Adding New Schools
1. Edit `backend/official_tvet_schools.py`
2. Add school with province and district
3. Run: `python seed_official_schools.py`

### Updating School Info
1. Modify school entry in `official_tvet_schools.py`
2. Re-run seed script
3. Changes applied immediately

## Support

- **Setup Issues**: Check `setup-official-tvet.bat` output
- **API Issues**: Visit `http://localhost:8000/docs`
- **Frontend Issues**: Check browser console
- **Database Issues**: Verify seed script ran successfully

---

**70 Official TVET/TSS Schools | Province → District → School Flow** 🎓
