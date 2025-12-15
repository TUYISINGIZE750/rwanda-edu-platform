# TVET Schools Integration Setup Guide

## Overview
This guide explains the integration of Rwanda's TVET (Technical and Vocational Education and Training) and TSS (Technical Secondary Schools) with the education platform, using real administrative locations.

## Features Implemented

### 1. Location-Based School System
- **Province → District → Sector → School** hierarchy
- Cascading dropdowns for location selection
- Real Rwanda administrative data from `locations.json`
- 40 TVET/TSS schools mapped to actual sectors

### 2. School Database
All schools include:
- School name
- Type (TVET or TSS)
- Category (Public, Private, Faith-Based)
- Location (Province, District, Sector)
- Available trades/programs

### 3. User Registration
Students and teachers register by:
1. Selecting their province
2. Selecting their district
3. Selecting their sector
4. Viewing and selecting from TVET/TSS schools in that sector
5. Completing registration with school-specific information

## Database Schema

### Schools Table
```sql
CREATE TABLE schools (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    type VARCHAR NOT NULL,  -- 'TVET' or 'TSS'
    category VARCHAR NOT NULL,  -- 'Public', 'Private', 'Faith-Based'
    province VARCHAR NOT NULL,
    district VARCHAR NOT NULL,
    sector VARCHAR NOT NULL,
    trades JSON  -- Array of available programs
);
```

### Users Table (Updated)
```sql
ALTER TABLE users ADD COLUMN province VARCHAR;
ALTER TABLE users ADD COLUMN district VARCHAR;
ALTER TABLE users ADD COLUMN sector VARCHAR;
```

## Setup Instructions

### 1. Database Migration
```bash
cd backend
python -m alembic upgrade head
```

### 2. Seed TVET Schools Data
```bash
cd backend
python seed_tvet_schools.py
```

This will populate the database with 40 TVET/TSS schools:
- 5 IPRC (Integrated Polytechnic Regional Centres)
- Multiple TSS schools across all provinces
- Private and faith-based TVET institutions

### 3. Verify Installation
```bash
# Check schools were seeded
python -c "from app.core.database import SessionLocal; from app.models.school import School; db = SessionLocal(); print(f'Total schools: {db.query(School).count()}')"
```

## API Endpoints

### Location Endpoints
- `GET /api/v1/api/locations/provinces` - Get all provinces
- `GET /api/v1/api/locations/districts/{province}` - Get districts in province
- `GET /api/v1/api/locations/sectors/{province}/{district}` - Get sectors in district

### School Endpoints
- `GET /api/v1/api/locations/schools/sector/{province}/{district}/{sector}` - Get schools in sector
- `GET /api/v1/api/locations/schools/district/{province}/{district}` - Get schools in district
- `GET /api/v1/api/locations/schools` - Get all schools

### Updated Auth Endpoints
- `POST /api/v1/auth/register` - Register with location and school selection

## Frontend Components

### RegisterView.vue
Complete registration form with:
- Personal information (name, email, password)
- Role selection (student/teacher)
- Cascading location dropdowns
- Dynamic school list based on selected sector
- Grade selection for students
- Language preference

### Translation Support
Full support for:
- English (en)
- French (fr)
- Kinyarwanda (rw)

## School Distribution

### By Province
- **Kigali City**: 5 schools
- **Southern Province**: 9 schools
- **Eastern Province**: 6 schools
- **Western Province**: 8 schools
- **Northern Province**: 6 schools

### By Type
- **TVET Schools**: 25
- **TSS Schools**: 15

### Major Institutions
1. IPRC Kigali (Kimironko)
2. IPRC Huye (Ngoma)
3. IPRC Musanze (Muhoza)
4. IPRC Ngoma (Kibungo)
5. IPRC Karongi (Bwishyura)
6. TSS Byimana (Ruhango)
7. TSS Murunda (Rwamagana)
8. TSS Rubengera (Karongi)
9. Don Bosco VTC Schools (Multiple locations)
10. Tumba College of Technology

## Data Source
Schools data is based on the official REB/WDA TVET schools list, ensuring:
- Accurate school names
- Correct administrative locations
- Real available trades/programs
- Current institutional categories

## Usage Flow

### Student/Teacher Registration
1. User visits `/register`
2. Enters personal information
3. Selects role (student/teacher)
4. Chooses province from dropdown
5. Chooses district (filtered by province)
6. Chooses sector (filtered by district)
7. Views TVET/TSS schools in selected sector
8. Selects their school
9. Students select grade (Year 1-3)
10. Selects language preference
11. Completes registration

### Login
1. User visits `/login`
2. Enters credentials
3. System validates and logs in
4. User data includes location and school information

## Benefits

1. **Accurate Data**: Real schools and locations
2. **Easy Navigation**: Cascading dropdowns guide users
3. **Location-Based**: Schools filtered by actual administrative boundaries
4. **Scalable**: Easy to add more schools
5. **Multilingual**: Full support for Rwanda's languages
6. **Comprehensive**: Covers all TVET/TSS institutions

## Maintenance

### Adding New Schools
1. Edit `backend/tvet_schools_data.py`
2. Add school entry with correct location mapping
3. Run seed script: `python seed_tvet_schools.py`

### Updating Locations
1. Update `rwanda-locations-json-master/locations.json`
2. Restart backend server
3. Location service will reload data automatically

## Testing

### Test Registration Flow
1. Start backend: `cd backend && uvicorn app.main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Navigate to `http://localhost:5173/register`
4. Test cascading dropdowns
5. Verify schools appear for selected sector
6. Complete registration
7. Verify user created with location data

### Test API Endpoints
```bash
# Get provinces
curl http://localhost:8000/api/v1/api/locations/provinces

# Get districts in Kigali
curl http://localhost:8000/api/v1/api/locations/districts/Umujyi%20wa%20Kigali

# Get schools in Kimironko sector
curl http://localhost:8000/api/v1/api/locations/schools/sector/Umujyi%20wa%20Kigali/Gasabo/Kimironko
```

## Troubleshooting

### No schools appearing
- Verify schools were seeded: Check database
- Check sector name matches exactly
- Ensure location hierarchy is correct

### Location dropdowns not working
- Verify `locations.json` path is correct
- Check LocationService is loading data
- Verify API endpoints are accessible

### Registration fails
- Check all required fields are filled
- Verify school_id is valid
- Check database constraints
- Review backend logs

## Future Enhancements

1. Add school contact information
2. Include school capacity data
3. Add program/trade details
4. Implement school search functionality
5. Add school profiles with photos
6. Include admission requirements
7. Add school performance metrics

## Support

For issues or questions:
1. Check logs: `backend/logs/`
2. Review API documentation: `http://localhost:8000/docs`
3. Verify database state
4. Check frontend console for errors
