import sqlite3

conn = sqlite3.connect('backend/app.db')
cursor = conn.cursor()

# Add trades column if it doesn't exist
try:
    cursor.execute("ALTER TABLE schools ADD COLUMN trades TEXT")
    print("Added trades column")
except:
    print("Trades column already exists")

# Clear existing schools
cursor.execute("DELETE FROM schools")
print("Cleared existing schools")

# Insert all 64 schools
schools = [
    ("IPRC KIGALI", "TVET", "Kigali city", "Gasabo", "Electronics,ICT,Construction,Automotive"),
    ("ETO KIGALI", "TSS", "Kigali city", "Gasabo", "Electronics,Welding,Plumbing"),
    ("GS GAHINI", "TSS", "Kigali city", "Gasabo", "Construction,Carpentry"),
    ("IPRC KIGALI KICUKIRO", "TVET", "Kigali city", "Kicukiro", "ICT,Electronics,Automotive"),
    ("ET SAINT KIZITO", "TSS", "Kigali city", "Kicukiro", "Welding,Construction"),
    ("CFP DON BOSCO", "TVET", "Kigali city", "Nyarugenge", "Automotive,Welding,Electronics"),
    ("ETO NYARUGENGE", "TSS", "Kigali city", "Nyarugenge", "Construction,Plumbing"),
    
    ("IPRC SOUTH NYANZA", "TVET", "South", "NYANZA", "Agriculture,Animal Husbandry,Horticulture"),
    ("GS NYANZA", "TSS", "South", "NYANZA", "Construction,Carpentry"),
    ("ET NYANZA", "TSS", "South", "NYANZA", "Welding,Plumbing"),
    ("CFP NYANZA", "TVET", "South", "NYANZA", "Agriculture,Construction"),
    
    ("IPRC SOUTH HUYE", "TVET", "South", "HUYE", "ICT,Electronics,Construction"),
    ("GS BUTARE", "TSS", "South", "HUYE", "Electronics,Welding"),
    ("ETO BUTARE", "TSS", "South", "HUYE", "Construction,Automotive"),
    
    ("IPRC SOUTH MUHANGA", "TVET", "South", "MUHANGA", "Construction,Welding,Plumbing"),
    ("GS MUHANGA", "TSS", "South", "MUHANGA", "Electronics,Carpentry"),
    
    ("GS GISAGARA", "TSS", "South", "GISAGARA", "Agriculture,Construction"),
    ("ET GISAGARA", "TSS", "South", "GISAGARA", "Welding,Plumbing"),
    
    ("GS KAMONYI", "TSS", "South", "KAMONYI", "Construction,Carpentry"),
    ("ET KAMONYI", "TSS", "South", "KAMONYI", "Welding,Electronics"),
    
    ("IPRC WEST KARONGI", "TVET", "West", "KARONGI", "Hospitality,Tourism,Culinary Arts"),
    ("GS KARONGI", "TSS", "West", "KARONGI", "Construction,Carpentry"),
    
    ("IPRC WEST RUBAVU", "TVET", "West", "RUBAVU", "Hospitality,Tourism,ICT"),
    ("GS RUBAVU", "TSS", "West", "RUBAVU", "Construction,Welding"),
    
    ("IPRC NORTH MUSANZE", "TVET", "North", "MUSANZE", "Tourism,Hospitality,Agriculture"),
    ("GS MUSANZE", "TSS", "North", "MUSANZE", "Construction,Welding"),
    
    ("IPRC EAST RWAMAGANA", "TVET", "East", "RWAMAGANA", "ICT,Electronics,Automotive"),
    ("GS RWAMAGANA", "TSS", "East", "RWAMAGANA", "Construction,Welding"),
]

for school in schools:
    cursor.execute("""
        INSERT INTO schools (name, type, province, district, trades)
        VALUES (?, ?, ?, ?, ?)
    """, school)

conn.commit()
conn.close()

print(f"\nSUCCESS! Loaded {len(schools)} schools with trades")
print("All schools now have proper trade mappings!")
