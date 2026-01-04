-- Step 1: Add missing columns
ALTER TABLE schools ADD COLUMN IF NOT EXISTS school_code VARCHAR;
ALTER TABLE schools ADD COLUMN IF NOT EXISTS gender VARCHAR;

-- Step 2: Verify columns exist
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'schools'
ORDER BY ordinal_position;

-- Step 3: Check current school count
SELECT COUNT(*) as school_count FROM schools;

-- Step 4: Check if any schools exist
SELECT id, name, district, province, 
       CASE WHEN trades IS NULL THEN 'NULL' ELSE jsonb_array_length(trades::jsonb)::text END as trade_count
FROM schools 
LIMIT 5;
