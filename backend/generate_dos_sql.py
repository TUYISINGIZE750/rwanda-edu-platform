import json
import bcrypt

# Load credentials
with open('dos_credentials_from_excel.json', 'r', encoding='utf-8') as f:
    credentials = json.load(f)

# Generate SQL
sql_statements = []
sql_statements.append("-- DOS Users from Excel - Generated SQL")
sql_statements.append("-- Run this on your Render PostgreSQL database\n")

for cred in credentials:
    # Hash password with bcrypt
    hashed_pw = bcrypt.hashpw(cred['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    email = cred['username'].replace("'", "''")
    full_name = f"DOS - {cred['school_name']}".replace("'", "''")
    school_code = cred['school_code']
    province = cred['province'].replace("'", "''")
    district = cred['district'].replace("'", "''")
    
    sql = f"""INSERT INTO users (email, hashed_password, full_name, role, school_id, province, district, is_active)
VALUES ('{email}', '{hashed_pw}', '{full_name.replace("'", "''")}', 'admin', {school_code}, '{province}', '{district}', 1)
ON CONFLICT (email) DO NOTHING;"""
    
    sql_statements.append(sql)

# Save to file
with open('insert_dos_users.sql', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(sql_statements))

print(f"Generated SQL for {len(credentials)} DOS users")
print("File: insert_dos_users.sql")
print("\nYou can run this SQL on your Render PostgreSQL database")
print("\nSample credentials:")
for i in range(min(5, len(credentials))):
    c = credentials[i]
    print(f"\nEmail: {c['username']}")
    print(f"Password: {c['password']}")
    print(f"School: {c['school_name']}")
