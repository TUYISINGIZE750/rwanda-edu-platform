"""Parse the real TVET Excel file"""
import pandas as pd
import json

file_path = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"

try:
    df = pd.read_excel(file_path, engine='openpyxl')
    
    print(f"Total rows: {len(df)}")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nFirst 3 rows:")
    print(df.head(3))
    
    # Save to JSON for inspection
    schools = []
    for idx, row in df.iterrows():
        school = {}
        for col in df.columns:
            val = row[col]
            if pd.notna(val):
                school[col] = str(val)
        if school:
            schools.append(school)
    
    with open("excel_data.json", "w", encoding="utf-8") as f:
        json.dump(schools[:5], f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Saved first 5 schools to excel_data.json")
    print(f"✓ Total schools found: {len(schools)}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
