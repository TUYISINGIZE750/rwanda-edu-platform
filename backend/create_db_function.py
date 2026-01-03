import psycopg2

DB_CONFIG = {
    'host': 'dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com',
    'port': 5432,
    'database': 'rwanda_edu_db',
    'user': 'rwanda_edu_db_user',
    'password': 'NJmoQ8ze9kV53DT6OB6AAMsa7qetokba'
}

print("Creating database function to serve schools...")

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# Create a function that returns schools as JSON
sql = """
CREATE OR REPLACE FUNCTION get_schools_by_district(p_province TEXT, p_district TEXT)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_agg(json_build_object(
        'id', id,
        'name', name,
        'type', type,
        'category', category,
        'province', province,
        'district', district,
        'trades', COALESCE(trades, '[]'::json)
    ))
    INTO result
    FROM schools
    WHERE LOWER(province) = LOWER(p_province)
    AND LOWER(district) = LOWER(p_district);
    
    RETURN COALESCE(result, '[]'::json);
END;
$$ LANGUAGE plpgsql;
"""

cursor.execute(sql)
conn.commit()

# Test it
cursor.execute("SELECT get_schools_by_district('South', 'Kamonyi')")
result = cursor.fetchone()[0]
print(f"\nTest result: {result}")

cursor.close()
conn.close()

print("\nDatabase function created!")
print("But this won't help - we need the backend code deployed.")
