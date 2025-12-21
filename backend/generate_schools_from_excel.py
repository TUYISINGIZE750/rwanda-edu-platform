"""Generate schools data from Excel file"""
import pandas as pd
from collections import defaultdict

file_path = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"

df = pd.read_excel(file_path, engine='openpyxl')

# Skip header row
df = df.iloc[1:]

# Group by school
schools_dict = defaultdict(lambda: {"trades": []})

for _, row in df.iterrows():
    province = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
    district = str(row.iloc[1]).strip().title() if pd.notna(row.iloc[1]) else ""  # Title case
    school_code = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ""
    school_name = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
    trade_full = str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else ""
    
    if not school_name or school_name == "nan":
        continue
    
    key = (province, district, school_code, school_name)
    
    if not schools_dict[key]["trades"]:
        schools_dict[key]["province"] = province
        schools_dict[key]["district"] = district
        schools_dict[key]["school_code"] = school_code
        schools_dict[key]["name"] = school_name
    
    if trade_full and trade_full != "nan":
        schools_dict[key]["trades"].append(trade_full)

# Convert to list
schools = []
for i, (key, data) in enumerate(schools_dict.items(), 1):
    school_type = "TVET" if "TVET" in data["name"].upper() else "TSS"
    category = "Public"
    
    schools.append({
        "id": i,
        "name": data["name"],
        "type": school_type,
        "category": category,
        "province": data["province"],
        "district": data["district"],
        "trades": ", ".join(data["trades"])
    })

print(f"Total unique schools: {len(schools)}")

# Write to Python file
with open("tvet_schools_data.py", "w", encoding="utf-8") as f:
    f.write('"""TVET and TSS Schools Data"""\n\n')
    f.write("TVET_TSS_SCHOOLS = [\n")
    for school in schools:
        f.write("    {\n")
        f.write(f'        "id": {school["id"]},\n')
        f.write(f'        "name": "{school["name"]}",\n')
        f.write(f'        "type": "{school["type"]}",\n')
        f.write(f'        "category": "{school["category"]}",\n')
        f.write(f'        "province": "{school["province"]}",\n')
        f.write(f'        "district": "{school["district"]}",\n')
        f.write(f'        "trades": "{school["trades"]}"\n')
        f.write("    },\n")
    f.write("]\n")

print(f"Generated tvet_schools_data.py with {len(schools)} schools")
