import psycopg2
import sys

# Your Render database connection details
# Get these from Render Dashboard -> Connect -> External Database URL
DB_CONFIG = {
    'host': 'dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com',
    'port': 5432,
    'database': 'rwanda_edu_db',
    'user': 'rwanda_edu_db_user',
    'password': 'NJmoQ8ze9kV53DT6OB6AAMsa7qetokba'
}

print("="*60)
print("Adding DOS Users to Render Database")
print("="*60)

try:
    # Connect to database
    print("\n1. Connecting to database...")
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("   [OK] Connected successfully!")
    
    # Read SQL file
    print("\n2. Reading SQL file...")
    with open('insert_dos_users.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()
    print("   [OK] SQL file loaded!")
    
    # Execute SQL
    print("\n3. Executing SQL (adding 190 DOS users)...")
    cursor.execute(sql_content)
    conn.commit()
    print("   [OK] SQL executed successfully!")
    
    # Verify
    print("\n4. Verifying...")
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
    count = cursor.fetchone()[0]
    print(f"   [OK] Total DOS users in database: {count}")
    
    # Show sample users
    print("\n5. Sample DOS users added:")
    cursor.execute("SELECT email, full_name, province, district FROM users WHERE role = 'admin' LIMIT 5")
    for row in cursor.fetchall():
        print(f"   - {row[0]}")
        print(f"     {row[1]} ({row[2]}, {row[3]})")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*60)
    print("SUCCESS! All DOS users added to remote database!")
    print("="*60)
    print("\nYou can now test login at:")
    print("https://tssanywhere.pages.dev/admin-login")
    print("\nTest credentials:")
    print("Email: nyamata_tvet_school_1@tssanywhere.rw")
    print("Password: dos12024")
    
except Exception as e:
    print(f"\n[ERROR]: {e}")
    print("\nPlease check:")
    print("1. Your password is correct in DB_CONFIG")
    print("2. Your IP is allowed in Render (0.0.0.0/0 is set)")
    print("3. You have internet connection")
    sys.exit(1)
