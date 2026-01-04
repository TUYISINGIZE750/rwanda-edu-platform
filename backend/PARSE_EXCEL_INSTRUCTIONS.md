# 🚀 Automated TVET Schools Excel Parser

## What This Does
Automatically reads the TVET schools Excel file using school codes for accurate identification, and updates all 164 schools in the database with their real trades from Ministry of Education data.

## Prerequisites
```bash
pip install pandas openpyxl sqlalchemy psycopg2-binary
```

## Quick Start

1. **Place Excel file** in `backend` directory (any TVET Excel file will be auto-detected)

2. **Run the parser**:
   ```bash
   cd backend
   python parse_schools_excel.py
   ```

3. **Enter database URL when prompted**:
   ```
   postgresql://rwanda_edu_db_user:NJmoQ8ze9kV53DT6OB6AAMsa7qetokba@dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com/rwanda_edu_db
   ```

## Features

✅ **Automatic Column Detection** - Finds school, trade, province, district columns automatically  
✅ **Smart Matching** - Uses exact and fuzzy matching to find schools in database  
✅ **Handles Any Format** - Skips header rows, handles merged cells, cleans data  
✅ **All 164 Schools** - Uses school codes to accurately identify and process every unique school  
✅ **Real Trades** - Updates with actual trades from Ministry of Education data  

## Expected Output
```
🚀 TVET Schools Excel Parser & Database Seeder
📖 Reading: 10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES...
   Found 493 rows
🔍 Detected columns:
   school: 'SCHOOL NAME'
   trade: 'TRADE'
   province: 'PROVINCE'
   district: 'DISTRICT'
📊 Parsed 164 unique schools (by school code)
✅ Updated 164/164 schools
🎯 RUNDA TVET School:
   Trades: {Software Development,Computer system and architecture,Land surveying,Building construction}
✅ SUCCESS! All schools updated with trades from Excel
```

## After Running
- All 164 TVET schools have real trades from Excel
- Teachers see actual trades in department dropdown
- No more fallback trades needed
- RUNDA TVET shows: Software Development, Computer Systems and Architecture, Land Surveying, Building Construction
