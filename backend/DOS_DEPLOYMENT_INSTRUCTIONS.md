# DOS Users Deployment Instructions

## Files Generated

1. **DOS_CREDENTIALS_BY_PROVINCE_DISTRICT_SCHOOL.pdf** - Professional PDF with all credentials
2. **dos_credentials_from_excel.json** - JSON file with all 190 DOS users
3. **insert_dos_users.sql** - SQL script to add all DOS users to database

## Deployment Steps

### Step 1: Add DOS Users to Remote Database

Go to your Render PostgreSQL database:
https://dashboard.render.com/

1. Click on your database: `rwanda_edu_db`
2. Click "Connect" → "External Connection"
3. Use the SQL editor or connect via psql
4. Run the SQL file: `insert_dos_users.sql`

### Step 2: Test DOS Login

Visit: https://tssanywhere.pages.dev/admin-login

**Test Credentials by Province:**

**East Province (32 schools):**
- Email: `nyamata_tvet_school_1@tssanywhere.rw`
- Password: `dos12024`
- School: NYAMATA TVET SCHOOL, District: BUGESERA

**Kigali City (5 schools):**
- Email: `forever_tvet_institu_33@tssanywhere.rw`
- Password: `dos332024`
- School: FOREVER TVET INSTITUTE, District: GASABO

**North Province (48 schools):**
- Email: `cepem_tvet_school_38@tssanywhere.rw`
- Password: `dos382024`
- School: CEPEM TVET SCHOOL, District: BURERA

**South Province (61 schools):**
- Email: `gikonko_tvet_school_86@tssanywhere.rw`
- Password: `dos862024`
- School: GIKONKO TVET SCHOOL, District: GISAGARA

**West Province (44 schools):**
- Email: `esa_birambo_147@tssanywhere.rw`
- Password: `dos1472024`
- School: ESA BIRAMBO, District: KARONGI

## Total Coverage

- **190 TVET Schools**
- **5 Provinces**
- **All Districts**
- Email format: `school_name_id@tssanywhere.rw`
- Password format: `dosID2024`

## Database Schema

```sql
users table:
- email (unique)
- hashed_password (bcrypt)
- full_name
- role ('admin' for DOS)
- school_id (from Excel school_code)
- province
- district
- is_active (1)
```

## Quick SQL Execution

```bash
# Connect to Render PostgreSQL
psql postgresql://rwanda_edu_db_user:PASSWORD@dpg-ctalmhij1k6c73f6pu50-a.oregon-postgres.render.com/rwanda_edu_db

# Run the SQL file
\i insert_dos_users.sql

# Verify
SELECT COUNT(*) FROM users WHERE role = 'admin';
```

## Notes

- All passwords are bcrypt hashed
- SQL uses `ON CONFLICT (email) DO NOTHING` to avoid duplicates
- Each DOS user is linked to their school via school_id
- Role is set to 'admin' for DOS users
