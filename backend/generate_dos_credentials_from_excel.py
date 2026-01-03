import pandas as pd
import json

# Read Excel file
df = pd.read_excel('10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx')

# Skip first row (header) and rename columns
df.columns = ['Province', 'District', 'School_Code', 'School_Name', 'Trade', 'Trade_Code', 'Gender']
df = df[1:]  # Skip the header row

# Get unique schools
schools = df.groupby(['Province', 'District', 'School_Code', 'School_Name']).size().reset_index()[['Province', 'District', 'School_Code', 'School_Name']]

credentials = []
for idx, row in schools.iterrows():
    province = str(row['Province']).strip()
    district = str(row['District']).strip()
    school_code = str(row['School_Code']).strip()
    school_name = str(row['School_Name']).strip()
    
    # Create email username from school name
    username = school_name.lower().replace(' ', '_').replace('-', '_')[:20] + f"_{idx+1}@tssanywhere.rw"
    
    credential = {
        "id": idx + 1,
        "username": username,
        "password": f"dos{idx+1}2024",
        "province": province,
        "district": district,
        "school_code": school_code,
        "school_name": school_name
    }
    credentials.append(credential)

# Save to JSON
with open('dos_credentials_from_excel.json', 'w', encoding='utf-8') as f:
    json.dump(credentials, f, indent=2, ensure_ascii=False)

print(f"Generated {len(credentials)} DOS credentials")
print("\nSample credentials:")
for i in range(min(10, len(credentials))):
    c = credentials[i]
    print(f"\nProvince: {c['province']}")
    print(f"District: {c['district']}")
    print(f"School: {c['school_name']}")
    print(f"Username: {c['username']}")
    print(f"Password: {c['password']}")
