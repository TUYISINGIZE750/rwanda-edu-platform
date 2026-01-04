"""
TVET Schools Excel Parser - Automatically detects structure and seeds database
Handles any Excel format with intelligent column detection
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os
import sys
import re

def clean_text(text):
    """Clean and normalize text"""
    if pd.isna(text) or text is None:
        return ""
    return str(text).strip()

def detect_columns(df):
    """Intelligently detect which columns contain school, trade, province, district"""
    columns = {}
    
    # Check each column for patterns
    for col in df.columns:
        col_lower = str(col).lower()
        sample_values = df[col].dropna().astype(str).head(20).tolist()
        sample_text = ' '.join(sample_values).lower()
        
        # Detect school column
        if any(word in col_lower for word in ['school', 'name', 'institution']) or \
           any(word in sample_text for word in ['tvet', 'school', 'college', 'centre']):
            if 'school' not in columns:
                columns['school'] = col
        
        # Detect trade/option column
        if any(word in col_lower for word in ['trade', 'option', 'course', 'program']) or \
           any(word in sample_text for word in ['construction', 'software', 'electronics', 'welding']):
            if 'trade' not in columns:
                columns['trade'] = col
        
        # Detect province column
        if any(word in col_lower for word in ['province', 'prov']) or \
           any(word in sample_text for word in ['kigali', 'eastern', 'western', 'northern', 'southern']):
            if 'province' not in columns:
                columns['province'] = col
        
        # Detect district column
        if any(word in col_lower for word in ['district', 'dist']):
            if 'district' not in columns:
                columns['district'] = col
    
    return columns

def parse_excel_smart(excel_file):
    """Smart Excel parser that handles any structure"""
    
    print(f"Reading: {excel_file}")
    
    # Try reading with skiprows=1 (header is in row 2)
    df = pd.read_excel(excel_file, skiprows=1)
    
    print(f"Found {len(df)} rows")
    print(f"\nColumns: {df.columns.tolist()}")
    
    # Parse schools and trades
    schools_data = {}
    
    for idx, row in df.iterrows():
        school_name = clean_text(row.get('School Name ', row.get('School Name', '')))
        trade = clean_text(row.get('Trade in full', row.get('Trade', '')))
        province = clean_text(row.get('Province', ''))
        district = clean_text(row.get('District ', row.get('District', '')))
        
        # Skip empty rows
        if not school_name or len(school_name) < 3:
            continue
        
        # Normalize school name
        school_name = re.sub(r'\s+', ' ', school_name)
        
        # Create unique key
        key = school_name.upper()
        
        if key not in schools_data:
            schools_data[key] = {
                'name': school_name,
                'province': province,
                'district': district,
                'trades': []
            }
        
        # Add trade if valid
        if trade and len(trade) > 2 and trade.lower() not in ['nan', 'none', 'n/a']:
            trade = re.sub(r'\s+', ' ', trade)
            if trade not in schools_data[key]['trades']:
                schools_data[key]['trades'].append(trade)
    
    return schools_data

def update_database(schools_data, database_url):
    """Update database with parsed schools and trades"""
    
    print(f"\nParsed {len(schools_data)} unique schools")
    
    # Show samples
    print("\nSample schools:")
    for i, (key, data) in enumerate(list(schools_data.items())[:5]):
        print(f"  {i+1}. {data['name']}")
        print(f"     Trades ({len(data['trades'])}): {', '.join(data['trades'][:3])}...")
    
    # Connect to database
    print(f"\nConnecting to database...")
    engine = create_engine(database_url)
    
    updated_count = 0
    not_found = []
    
    with engine.connect() as conn:
        for key, data in schools_data.items():
            if not data['trades']:
                continue
            
            school_name = data['name']
            
            # Create PostgreSQL array literal
            trades_list = data['trades']
            
            # Try exact match first
            result = conn.execute(text("""
                UPDATE schools 
                SET trades = ARRAY[:trades]
                WHERE LOWER(TRIM(name)) = LOWER(TRIM(:name))
                RETURNING id, name
            """), {"trades": trades_list, "name": school_name})
            
            updated = result.fetchone()
            
            # Try fuzzy match if exact fails
            if not updated:
                # Extract key words from school name
                words = school_name.upper().split()
                main_words = [w for w in words if len(w) > 3 and w not in ['TVET', 'SCHOOL', 'CENTRE', 'CENTER']]
                
                if main_words:
                    search_pattern = '%' + '%'.join(main_words[:2]) + '%'
                    result = conn.execute(text("""
                        UPDATE schools 
                        SET trades = ARRAY[:trades]
                        WHERE UPPER(name) LIKE :pattern
                        RETURNING id, name
                    """), {"trades": trades_list, "pattern": search_pattern})
                    
                    updated = result.fetchone()
            
            if updated:
                updated_count += 1
                if updated_count <= 3 or 'RUNDA' in school_name.upper():
                    print(f"  [OK] {updated[1]} -> {len(data['trades'])} trades")
            else:
                not_found.append(school_name)
        
        conn.commit()
    
    print(f"\n{'='*60}")
    print(f"[SUCCESS] Updated {updated_count} schools with trades")
    print(f"[WARNING] {len(not_found)} schools not found in database")
    
    if not_found and len(not_found) <= 10:
        print(f"\nNot found in database:")
        for name in not_found[:10]:
            print(f"  - {name}")
    
    # Show RUNDA TVET result
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, name, province, district, trades
            FROM schools
            WHERE UPPER(name) LIKE '%RUNDA%'
        """))
        
        runda = result.fetchall()
        if runda:
            print(f"\n{'='*60}")
            print("RUNDA TVET School:")
            for school in runda:
                print(f"  ID: {school[0]}")
                print(f"  Name: {school[1]}")
                print(f"  Location: {school[2]}, {school[3]}")
                print(f"  Trades: {school[4]}")

if __name__ == "__main__":
    print("="*60)
    print("  TVET Schools Excel Parser & Database Seeder")
    print("="*60)
    
    # Get database URL
    if len(sys.argv) > 1:
        DATABASE_URL = sys.argv[1]
    else:
        DATABASE_URL = os.getenv("DATABASE_URL")
        if not DATABASE_URL:
            print("\nUsage: python parse_schools_excel.py [DATABASE_URL]")
            DATABASE_URL = input("\nEnter DATABASE_URL: ").strip()
    
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # Find Excel file
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx') and 'TVET' in f.upper()]
    
    if not excel_files:
        print("\n[ERROR] No TVET Excel file found in current directory")
        print("Please place the Excel file here and run again")
        sys.exit(1)
    
    excel_file = excel_files[0]
    
    try:
        schools_data = parse_excel_smart(excel_file)
        update_database(schools_data, DATABASE_URL)
        print("\n" + "="*60)
        print("[SUCCESS] All schools updated with trades from Excel")
        print("="*60)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
