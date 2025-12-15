import sqlite3

conn = sqlite3.connect('backend/app.db')
cursor = conn.cursor()

# Clear existing schools
cursor.execute("DELETE FROM schools")
print("Cleared existing schools")

# Insert all schools with proper schema
schools = [
    ("IPRC KIGALI", "TVET", "Public", "Kigali city", "Gasabo", "Electronics,ICT,Construction,Automotive"),
    ("ETO KIGALI", "TSS", "Public", "Kigali city", "Gasabo", "Electronics,Welding,Plumbing"),
    ("GS GAHINI", "TSS", "Public", "Kigali city", "Gasabo", "Construction,Carpentry"),
    ("IPRC KIGALI KICUKIRO", "TVET", "Public", "Kigali city", "Kicukiro", "ICT,Electronics,Automotive"),
    ("ET SAINT KIZITO", "TSS", "Private", "Kigali city", "Kicukiro", "Welding,Construction"),
    ("CFP DON BOSCO", "TVET", "Private", "Kigali city", "Nyarugenge", "Automotive,Welding,Electronics"),
    ("ETO NYARUGENGE", "TSS", "Public", "Kigali city", "Nyarugenge", "Construction,Plumbing"),
    
    ("IPRC SOUTH NYANZA", "TVET", "Public", "South", "NYANZA", "Agriculture,Animal Husbandry,Horticulture"),
    ("GS NYANZA", "TSS", "Public", "South", "NYANZA", "Construction,Carpentry"),
    ("ET NYANZA", "TSS", "Public", "South", "NYANZA", "Welding,Plumbing"),
    ("CFP NYANZA", "TVET", "Public", "South", "NYANZA", "Agriculture,Construction"),
    
    ("IPRC SOUTH HUYE", "TVET", "Public", "South", "HUYE", "ICT,Electronics,Construction"),
    ("GS BUTARE", "TSS", "Public", "South", "HUYE", "Electronics,Welding"),
    ("ETO BUTARE", "TSS", "Public", "South", "HUYE", "Construction,Automotive"),
    
    ("IPRC SOUTH MUHANGA", "TVET", "Public", "South", "MUHANGA", "Construction,Welding,Plumbing"),
    ("GS MUHANGA", "TSS", "Public", "South", "MUHANGA", "Electronics,Carpentry"),
    
    ("GS GISAGARA", "TSS", "Public", "South", "GISAGARA", "Agriculture,Construction"),
    ("ET GISAGARA", "TSS", "Public", "South", "GISAGARA", "Welding,Plumbing"),
    
    ("GS KAMONYI", "TSS", "Public", "South", "KAMONYI", "Construction,Carpentry"),
    ("ET KAMONYI", "TSS", "Public", "South", "KAMONYI", "Welding,Electronics"),
    
    ("IPRC WEST KARONGI", "TVET", "Public", "West", "KARONGI", "Hospitality,Tourism,Culinary Arts"),
    ("GS KARONGI", "TSS", "Public", "West", "KARONGI", "Construction,Carpentry"),
    
    ("IPRC WEST RUBAVU", "TVET", "Public", "West", "RUBAVU", "Hospitality,Tourism,ICT"),
    ("GS RUBAVU", "TSS", "Public", "West", "RUBAVU", "Construction,Welding"),
    
    ("IPRC NORTH MUSANZE", "TVET", "Public", "North", "MUSANZE", "Tourism,Hospitality,Agriculture"),
    ("GS MUSANZE", "TSS", "Public", "North", "MUSANZE", "Construction,Welding"),
    
    ("IPRC EAST RWAMAGANA", "TVET", "Public", "East", "RWAMAGANA", "ICT,Electronics,Automotive"),
    ("GS RWAMAGANA", "TSS", "Public", "East", "RWAMAGANA", "Construction,Welding"),
]

for school in schools:
    cursor.execute("""
        INSERT INTO schools (name, type, category, province, district, trades)
        VALUES (?, ?, ?, ?, ?, ?)
    """, school)

conn.commit()
conn.close()

print(f"\nSUCCESS! Loaded {len(schools)} schools")
print("\nSchools by Province:")
print("- Kigali City: 7 schools")
print("- South: 13 schools")
print("- West: 4 schools")
print("- North: 2 schools")
print("- East: 2 schools")
print(f"\nTotal: {len(schools)} TVET/TSS schools with trade mappings!")
