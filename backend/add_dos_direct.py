import psycopg2
import json
import bcrypt

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

# Load credentials
with open('dos_credentials_from_excel.json', 'r', encoding='utf-8') as f:
    credentials = json.load(f)

try:
    print("\n1. Connecting to database...")
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("   [OK] Connected!")
    
    print(f"\n2. Adding {len(credentials)} DOS users...")
    
    added = 0
    skipped = 0
    
    for idx, cred in enumerate(credentials, 1):
        try:
            # Hash password
            hashed_pw = bcrypt.hashpw(cred['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Insert user
            cursor.execute("""
                INSERT INTO users (email, hashed_password, full_name, role, school_id, province, district, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING
            """, (
                cred['username'],
                hashed_pw,
                f"DOS - {cred['school_name']}",
                'ADMIN',
                int(cred['school_code']),
                cred['province'],
                cred['district'],
                1
            ))
            
            if cursor.rowcount > 0:
                added += 1
            else:
                skipped += 1
            
            if idx % 20 == 0:
                conn.commit()
                print(f"   Progress: {idx}/{len(credentials)}...")
        
        except Exception as e:
            print(f"   [SKIP] {cred['username']}: {str(e)[:50]}")
            skipped += 1
    
    conn.commit()
    
    print(f"\n3. Verifying...")
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'ADMIN'")
    total = cursor.fetchone()[0]
    
    print("\n" + "="*60)
    print("SUCCESS!")
    print("="*60)
    print(f"Added: {added} new DOS users")
    print(f"Skipped: {skipped} (already exist or errors)")
    print(f"Total DOS in database: {total}")
    
    print("\n" + "="*60)
    print("Test Login at: https://tssanywhere.pages.dev/admin-login")
    print("="*60)
    print("\nSample Credentials:")
    for i in range(min(5, len(credentials))):
        c = credentials[i]
        print(f"\n{c['province']} - {c['district']}")
        print(f"  Email: {c['username']}")
        print(f"  Password: {c['password']}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n[ERROR]: {e}")
    import traceback
    traceback.print_exc()
