"""Parse official TVET schools Excel file and extract schools with trades"""
import pandas as pd
import json

def parse_tvet_excel():
    """Parse the official TVET schools Excel file"""
    file_path = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"
    
    try:
        df = pd.read_excel(file_path)
        
        schools_data = []
        school_id = 1
        
        for _, row in df.iterrows():
            school_info = {
                "id": school_id,
                "name": str(row.get("School Name", row.iloc[0])).strip() if pd.notna(row.get("School Name", row.iloc[0])) else "",
                "type": str(row.get("Type", "TVET")).strip() if pd.notna(row.get("Type")) else "TVET",
                "category": str(row.get("Category", "Public")).strip() if pd.notna(row.get("Category")) else "Public",
                "province": str(row.get("Province", row.iloc[1])).strip() if pd.notna(row.get("Province", row.iloc[1])) else "",
                "district": str(row.get("District", row.iloc[2])).strip() if pd.notna(row.get("District", row.iloc[2])) else "",
                "trades": []
            }
            
            # Extract trades from remaining columns
            for col in df.columns[3:]:
                trade = row.get(col)
                if pd.notna(trade) and str(trade).strip():
                    school_info["trades"].append(str(trade).strip())
            
            if school_info["name"]:
                schools_data.append(school_info)
                school_id += 1
        
        # Save to JSON
        with open("official_tvet_schools.json", "w", encoding="utf-8") as f:
            json.dump(schools_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Parsed {len(schools_data)} schools from Excel")
        return schools_data
        
    except Exception as e:
        print(f"Error parsing Excel: {e}")
        return []

if __name__ == "__main__":
    schools = parse_tvet_excel()
    print(f"\nTotal schools: {len(schools)}")
