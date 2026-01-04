import pandas as pd
from collections import defaultdict

file_path = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"

df = pd.read_excel(file_path, header=1)
print(f"Total rows: {len(df)}")
print(f"Raw columns: {list(df.columns)}")

# Clean column names
df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]
print(f"\nCleaned columns: {list(df.columns)}")

# Group by school
schools_data = defaultdict(lambda: {
    'trades': [],
    'school_code': None,
    'name': None,
    'province': None,
    'district': None,
    'gender': None
})

for idx, row in df.iterrows():
    if pd.isna(row['School Name']) or pd.isna(row['District']):
        continue
    
    school_key = (str(row['School Name']).strip(), str(row['District']).strip())
    school_data = schools_data[school_key]
    
    school_data['school_code'] = str(row['School code']).strip() if pd.notna(row['School code']) else None
    school_data['name'] = str(row['School Name']).strip()
    school_data['province'] = str(row['Province']).strip()
    school_data['district'] = str(row['District']).strip()
    school_data['gender'] = str(row['Gender']).strip() if pd.notna(row['Gender']) else 'Mixt'
    
    if pd.notna(row['Trade in full']):
        trade = str(row['Trade in full']).strip()
        if trade and trade not in school_data['trades']:
            school_data['trades'].append(trade)

print(f"\nTotal unique schools: {len(schools_data)}")

# Show schools in South/Kamonyi
print("\n=== Schools in South/Kamonyi ===")
for (name, district), data in schools_data.items():
    if data['province'] == 'South' and data['district'] == 'Kamonyi':
        print(f"{name} - {len(data['trades'])} trades: {data['trades']}")

# Show schools in South/Muhanga
print("\n=== Schools in South/Muhanga ===")
for (name, district), data in schools_data.items():
    if data['province'] == 'South' and data['district'] == 'Muhanga':
        print(f"{name} - {len(data['trades'])} trades: {data['trades']}")

# Show RUNDA TVET
print("\n=== RUNDA TVET ===")
for (name, district), data in schools_data.items():
    if 'RUNDA' in name.upper():
        print(f"{name} ({data['district']}, {data['province']})")
        print(f"  Trades ({len(data['trades'])}): {data['trades']}")
