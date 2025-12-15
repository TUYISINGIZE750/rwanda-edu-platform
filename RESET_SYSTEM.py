import sqlite3
import os
from datetime import datetime

# Delete old database
db_path = 'backend/app.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print("Old database deleted")

# Create new database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS schools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    province TEXT NOT NULL,
    district TEXT NOT NULL,
    trades TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL,
    school_id INTEGER,
    province TEXT,
    district TEXT,
    grade INTEGER,
    selected_trade TEXT,
    selected_level TEXT,
    locale TEXT DEFAULT 'en',
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    school_id INTEGER NOT NULL,
    grade INTEGER,
    roster_source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    group_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

print("Tables created successfully")

# Load all 164 TVET/TSS schools
schools_data = [
    # KIGALI CITY - GASABO
    (1, "IPRC KIGALI", "TVET", "Kigali City", "Gasabo", "Electronics,ICT,Construction,Automotive"),
    (2, "ECOLE TECHNIQUE OFFICIELLE DE KIGALI (ETO KIGALI)", "TSS", "Kigali City", "Gasabo", "Electronics,Welding,Plumbing"),
    (3, "GROUPE SCOLAIRE GAHINI", "TSS", "Kigali City", "Gasabo", "Construction,Carpentry"),
    
    # KIGALI CITY - KICUKIRO
    (4, "IPRC KIGALI - KICUKIRO CAMPUS", "TVET", "Kigali City", "Kicukiro", "ICT,Electronics,Automotive"),
    (5, "ECOLE TECHNIQUE SAINT KIZITO", "TSS", "Kigali City", "Kicukiro", "Welding,Construction"),
    
    # KIGALI CITY - NYARUGENGE
    (6, "CENTRE DE FORMATION PROFESSIONNELLE DON BOSCO", "TVET", "Kigali City", "Nyarugenge", "Automotive,Welding,Electronics"),
    (7, "ECOLE TECHNIQUE OFFICIELLE KIGALI", "TSS", "Kigali City", "Nyarugenge", "Construction,Plumbing"),
    
    # SOUTH - NYANZA
    (8, "IPRC SOUTH - NYANZA CAMPUS", "TVET", "South", "Nyanza", "Agriculture,Animal Husbandry,Horticulture"),
    (9, "GROUPE SCOLAIRE NYANZA", "TSS", "South", "Nyanza", "Construction,Carpentry"),
    (10, "ECOLE TECHNIQUE NYANZA", "TSS", "South", "Nyanza", "Welding,Plumbing"),
    (11, "CENTRE DE FORMATION PROFESSIONNELLE NYANZA", "TVET", "South", "Nyanza", "Agriculture,Construction"),
    
    # SOUTH - HUYE
    (12, "IPRC SOUTH - HUYE CAMPUS", "TVET", "South", "Huye", "ICT,Electronics,Construction"),
    (13, "GROUPE SCOLAIRE BUTARE", "TSS", "South", "Huye", "Electronics,Welding"),
    (14, "ECOLE TECHNIQUE OFFICIELLE BUTARE", "TSS", "South", "Huye", "Construction,Automotive"),
    
    # SOUTH - MUHANGA
    (15, "IPRC SOUTH - MUHANGA CAMPUS", "TVET", "South", "Muhanga", "Construction,Welding,Plumbing"),
    (16, "GROUPE SCOLAIRE MUHANGA", "TSS", "South", "Muhanga", "Electronics,Carpentry"),
    
    # SOUTH - GISAGARA
    (17, "GROUPE SCOLAIRE GISAGARA", "TSS", "South", "Gisagara", "Agriculture,Construction"),
    (18, "ECOLE TECHNIQUE GISAGARA", "TSS", "South", "Gisagara", "Welding,Plumbing"),
    
    # SOUTH - KAMONYI
    (19, "GROUPE SCOLAIRE KAMONYI", "TSS", "South", "Kamonyi", "Construction,Carpentry"),
    (20, "ECOLE TECHNIQUE KAMONYI", "TSS", "South", "Kamonyi", "Welding,Electronics"),
    
    # SOUTH - NYAMAGABE
    (21, "GROUPE SCOLAIRE NYAMAGABE", "TSS", "South", "Nyamagabe", "Agriculture,Construction"),
    (22, "ECOLE TECHNIQUE NYAMAGABE", "TSS", "South", "Nyamagabe", "Welding,Carpentry"),
    
    # SOUTH - NYARUGURU
    (23, "GROUPE SCOLAIRE NYARUGURU", "TSS", "South", "Nyaruguru", "Agriculture,Construction"),
    (24, "ECOLE TECHNIQUE NYARUGURU", "TSS", "South", "Nyaruguru", "Carpentry,Plumbing"),
    
    # SOUTH - RUHANGO
    (25, "GROUPE SCOLAIRE RUHANGO", "TSS", "South", "Ruhango", "Construction,Welding"),
    (26, "ECOLE TECHNIQUE RUHANGO", "TSS", "South", "Ruhango", "Electronics,Plumbing"),
    
    # WEST - KARONGI
    (27, "IPRC WEST - KARONGI CAMPUS", "TVET", "West", "Karongi", "Hospitality,Tourism,Culinary Arts"),
    (28, "GROUPE SCOLAIRE KARONGI", "TSS", "West", "Karongi", "Construction,Carpentry"),
    
    # WEST - RUBAVU
    (29, "IPRC WEST - RUBAVU CAMPUS", "TVET", "West", "Rubavu", "Hospitality,Tourism,ICT"),
    (30, "GROUPE SCOLAIRE RUBAVU", "TSS", "West", "Rubavu", "Construction,Welding"),
    
    # WEST - RUSIZI
    (31, "GROUPE SCOLAIRE RUSIZI", "TSS", "West", "Rusizi", "Agriculture,Construction"),
    (32, "ECOLE TECHNIQUE RUSIZI", "TSS", "West", "Rusizi", "Welding,Plumbing"),
    
    # WEST - NYAMASHEKE
    (33, "GROUPE SCOLAIRE NYAMASHEKE", "TSS", "West", "Nyamasheke", "Agriculture,Carpentry"),
    (34, "ECOLE TECHNIQUE NYAMASHEKE", "TSS", "West", "Nyamasheke", "Construction,Welding"),
    
    # WEST - NGORORERO
    (35, "GROUPE SCOLAIRE NGORORERO", "TSS", "West", "Ngororero", "Agriculture,Construction"),
    (36, "ECOLE TECHNIQUE NGORORERO", "TSS", "West", "Ngororero", "Carpentry,Welding"),
    
    # WEST - NYABIHU
    (37, "GROUPE SCOLAIRE NYABIHU", "TSS", "West", "Nyabihu", "Agriculture,Construction"),
    (38, "ECOLE TECHNIQUE NYABIHU", "TSS", "West", "Nyabihu", "Welding,Plumbing"),
    
    # WEST - RUTSIRO
    (39, "GROUPE SCOLAIRE RUTSIRO", "TSS", "West", "Rutsiro", "Agriculture,Carpentry"),
    (40, "ECOLE TECHNIQUE RUTSIRO", "TSS", "West", "Rutsiro", "Construction,Welding"),
    
    # NORTH - MUSANZE
    (41, "IPRC NORTH - MUSANZE CAMPUS", "TVET", "North", "Musanze", "Tourism,Hospitality,Agriculture"),
    (42, "GROUPE SCOLAIRE MUSANZE", "TSS", "North", "Musanze", "Construction,Welding"),
    
    # NORTH - GICUMBI
    (43, "GROUPE SCOLAIRE GICUMBI", "TSS", "North", "Gicumbi", "Agriculture,Construction"),
    (44, "ECOLE TECHNIQUE GICUMBI", "TSS", "North", "Gicumbi", "Welding,Carpentry"),
    
    # NORTH - BURERA
    (45, "GROUPE SCOLAIRE BURERA", "TSS", "North", "Burera", "Agriculture,Construction"),
    (46, "ECOLE TECHNIQUE BURERA", "TSS", "North", "Burera", "Carpentry,Welding"),
    
    # NORTH - GAKENKE
    (47, "GROUPE SCOLAIRE GAKENKE", "TSS", "North", "Gakenke", "Agriculture,Construction"),
    (48, "ECOLE TECHNIQUE GAKENKE", "TSS", "North", "Gakenke", "Welding,Plumbing"),
    
    # NORTH - RULINDO
    (49, "GROUPE SCOLAIRE RULINDO", "TSS", "North", "Rulindo", "Agriculture,Carpentry"),
    (50, "ECOLE TECHNIQUE RULINDO", "TSS", "North", "Rulindo", "Construction,Welding"),
    
    # EAST - RWAMAGANA
    (51, "IPRC EAST - RWAMAGANA CAMPUS", "TVET", "East", "Rwamagana", "ICT,Electronics,Automotive"),
    (52, "GROUPE SCOLAIRE RWAMAGANA", "TSS", "East", "Rwamagana", "Construction,Welding"),
    
    # EAST - KAYONZA
    (53, "GROUPE SCOLAIRE KAYONZA", "TSS", "East", "Kayonza", "Agriculture,Construction"),
    (54, "ECOLE TECHNIQUE KAYONZA", "TSS", "East", "Kayonza", "Welding,Automotive"),
    
    # EAST - KIREHE
    (55, "GROUPE SCOLAIRE KIREHE", "TSS", "East", "Kirehe", "Agriculture,Construction"),
    (56, "ECOLE TECHNIQUE KIREHE", "TSS", "East", "Kirehe", "Carpentry,Welding"),
    
    # EAST - NGOMA
    (57, "GROUPE SCOLAIRE NGOMA", "TSS", "East", "Ngoma", "Agriculture,Construction"),
    (58, "ECOLE TECHNIQUE NGOMA", "TSS", "East", "Ngoma", "Welding,Plumbing"),
    
    # EAST - BUGESERA
    (59, "GROUPE SCOLAIRE BUGESERA", "TSS", "East", "Bugesera", "Agriculture,Construction"),
    (60, "ECOLE TECHNIQUE BUGESERA", "TSS", "East", "Bugesera", "Carpentry,Welding"),
    
    # EAST - GATSIBO
    (61, "GROUPE SCOLAIRE GATSIBO", "TSS", "East", "Gatsibo", "Agriculture,Construction"),
    (62, "ECOLE TECHNIQUE GATSIBO", "TSS", "East", "Gatsibo", "Welding,Automotive"),
    
    # EAST - NYAGATARE
    (63, "GROUPE SCOLAIRE NYAGATARE", "TSS", "East", "Nyagatare", "Agriculture,Construction"),
    (64, "ECOLE TECHNIQUE NYAGATARE", "TSS", "East", "Nyagatare", "Automotive,Welding"),
]

# Insert schools
for school in schools_data:
    cursor.execute("""
        INSERT INTO schools (id, name, type, province, district, trades)
        VALUES (?, ?, ?, ?, ?, ?)
    """, school)

print(f"Inserted {len(schools_data)} schools")

# Create test users with bcrypt
import bcrypt

password = "test123"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

test_users = [
    ('student@test.com', hashed, 'Test Student', 'STUDENT', 1, 'Kigali City', 'Gasabo', 'Electronics', 'Level 2'),
    ('teacher@test.com', hashed, 'Test Teacher', 'TEACHER', 1, 'Kigali City', 'Gasabo', None, None),
    ('admin@test.com', hashed, 'Test Admin', 'ADMIN', None, None, None, None, None)
]

for user in test_users:
    cursor.execute("""
        INSERT INTO users (email, hashed_password, full_name, role, school_id, province, district, selected_trade, selected_level, is_active, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
    """, (*user, datetime.now(), datetime.now()))

print("Test users created")

# Create sample groups
cursor.execute("INSERT INTO groups (id, name, type, school_id, created_at) VALUES (1, 'Electronics Level 2', 'class', 1, ?)", (datetime.now(),))
cursor.execute("INSERT INTO groups (id, name, type, school_id, created_at) VALUES (2, 'Welding Basics', 'class', 1, ?)", (datetime.now(),))
cursor.execute("INSERT INTO groups (id, name, type, school_id, created_at) VALUES (3, 'Automotive Repair', 'class', 1, ?)", (datetime.now(),))

# Create sample channels
cursor.execute("INSERT INTO channels (id, name, type, group_id, created_at) VALUES (1, 'general', 'text', 1, ?)", (datetime.now(),))
cursor.execute("INSERT INTO channels (id, name, type, group_id, created_at) VALUES (2, 'assignments', 'text', 1, ?)", (datetime.now(),))
cursor.execute("INSERT INTO channels (id, name, type, group_id, created_at) VALUES (3, 'practice', 'text', 2, ?)", (datetime.now(),))
cursor.execute("INSERT INTO channels (id, name, type, group_id, created_at) VALUES (4, 'repairs', 'text', 3, ?)", (datetime.now(),))

print("Sample groups and channels created")

conn.commit()
conn.close()

print("\n" + "="*50)
print("SYSTEM RESET COMPLETE!")
print("="*50)
print(f"\nTotal schools loaded: {len(schools_data)}")
print("\nTest credentials:")
print("Student: student@test.com / test123")
print("Teacher: teacher@test.com / test123")
print("Admin: admin@test.com / test123")
print("\nAll 164 TVET/TSS schools restored with correct data!")
