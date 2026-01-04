# How to Parse Excel and Seed Schools with Trades

## Prerequisites
```bash
pip install pandas openpyxl sqlalchemy psycopg2-binary
```

## Steps

1. **Place the Excel file** in the `backend` directory:
   - File: `10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx`

2. **Run the script**:
   ```bash
   cd backend
   python parse_schools_excel.py
   ```

3. **When prompted, paste your database URL**:
   ```
   postgresql://rwanda_edu_db_user:NJmoQ8ze9kV53DT6OB6AAMsa7qetokba@dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com/rwanda_edu_db
   ```

## What it does:
1. Reads the Excel file
2. Groups trades by school name
3. Updates each school in the database with its trades array
4. Shows RUNDA TVET trades specifically

## Expected Output:
```
Parsed 165 unique schools
✓ Updated: RUNDA TVET
  Trades: ['Software Development', 'Computer Systems and Architecture', 'Land Surveying', ...]
✓ Updated 165 schools with trades
```

## After running:
- Teachers at RUNDA TVET will see real trades in dropdown
- All 165 schools will have their actual trades from Excel
- No more fallback trades needed
