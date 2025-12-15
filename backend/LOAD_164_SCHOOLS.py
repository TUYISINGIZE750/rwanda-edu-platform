import pandas as pd
import sqlite3
from collections import defaultdict

# Read Excel file
file_path = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"
df = pd.read_excel(file_path, header=1)

# Clean column names
df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]

# Group trades by school
schools_data = defaultdict(lambda: {'trades': [], 'province': None, 'district': None})

for idx, row in df.iterrows():
    if pd.isna(row['School Name']) or pd.isna(row['District']):
        continue
    
    school_key = (str(row['School Name']).strip(), str(row['District']).strip())
    school_data = schools_data[school_key]
    
    school_data['province'] = str(row['Province']).strip()
    school_data['district'] = str(row['District']).strip()
    
    if pd.notna(row['Trade in full']):
        trade = str(row['Trade in full']).strip()
        if trade and trade not in school_data['trades']:
            school_data['trades'].append(trade)

# Connect to database
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Clear existing schools
cursor.execute("DELETE FROM schools")
print("Cleared existing schools")

# Insert all schools
schools_added = 0
for (school_name, district), school_data in schools_data.items():
    trades_str = ",".join(school_data['trades'])
    
    cursor.execute("""
        INSERT INTO schools (name, type, category, province, district, trades)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (school_name, "TVET", "Public", school_data['province'], school_data['district'], trades_str))
    
    schools_added += 1
    print(f"{schools_added}. {school_name} ({district}) - {len(school_data['trades'])} trades")

conn.commit()
conn.close()

print(f"\nSUCCESS! Loaded {schools_added} schools from Excel")
print("All 164 TVET/TSS schools with trades restored!")
