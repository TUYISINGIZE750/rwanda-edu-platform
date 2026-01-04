import psycopg2

DATABASE_URL = "postgresql://rwanda_edu_platform_user:Uw0Ks0Hy0Ks0Hy0Ks0Hy0Ks0Hy0Ks0H@dpg-cu0bnhm8ii6s73a5rvog-a.oregon-postgres.render.com:5432/rwanda_edu_platform"

print("Connecting to database...")
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

print("Adding missing columns...")
cur.execute("ALTER TABLE schools ADD COLUMN IF NOT EXISTS school_code VARCHAR")
cur.execute("ALTER TABLE schools ADD COLUMN IF NOT EXISTS gender VARCHAR")
conn.commit()

print("Verifying columns...")
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'schools'")
columns = [row[0] for row in cur.fetchall()]
print(f"Columns in schools table: {columns}")

cur.close()
conn.close()

print("\nDone! Now trigger the reload endpoint:")
print("curl -X POST https://rwanda-edu-platform.onrender.com/api/v1/admin/schools/reload-from-excel")
