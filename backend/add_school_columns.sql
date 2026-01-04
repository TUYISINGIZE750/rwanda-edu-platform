-- Add missing columns to schools table
ALTER TABLE schools ADD COLUMN IF NOT EXISTS school_code VARCHAR;
ALTER TABLE schools ADD COLUMN IF NOT EXISTS gender VARCHAR;

-- Verify columns exist
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'schools';
