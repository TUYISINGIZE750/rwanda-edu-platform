"""Reload TVET schools to production database"""
import os
import sys
sys.path.append(os.path.dirname(__file__))

import pandas as pd
from collections import defaultdict
import psycopg2
from psycopg2.extras import Json

# Production database URL (external)
DATABASE_URL = "postgresql://rwanda_edu_platform_user:Uw0Ks0Hy0Ks0Hy0Ks0Hy0Ks0Hy0Ks0H@dpg-cu0bnhm8ii6s73a5rvog-a.oregon-postgres.render.com:5432/rwanda_edu_platform"

def reload_schools():
    """Reload schools from Excel to production database"""
    file_path = "10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx"
    
    if not os.path.exists(file_path):
        print(f"Excel file not found: {file_path}")
        return
    
    print("Reading Excel file...")
    df = pd.read_excel(file_path, header=1)
    print(f"Found {len(df)} rows")
    
    # Clean column names
    df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]
    
    # Connect to production database
    print("\nConnecting to production database...")
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    
    # Group trades by school
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
    
    # Clear existing schools
    print("\nClearing existing schools...")
    cur.execute("DELETE FROM schools")
    conn.commit()
    
    # Insert schools
    print("\nInserting schools...")
    schools_added = 0
    
    for (school_name, district), school_data in schools_data.items():
        cur.execute("""
            INSERT INTO schools (school_code, name, type, category, province, district, trades, gender)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            school_data['school_code'],
            school_data['name'],
            'TVET',
            'Public',
            school_data['province'],
            school_data['district'],
            Json(school_data['trades']),
            school_data['gender']
        ))
        schools_added += 1
        print(f"  {schools_added}. {school_data['name']} ({school_data['district']}) - {len(school_data['trades'])} trades")
    
    conn.commit()
    
    # Verify RUNDA TVET
    print("\n" + "="*60)
    print("Verifying RUNDA TVET (should have 4 trades):")
    cur.execute("SELECT id, name, district, trades FROM schools WHERE name ILIKE '%RUNDA%'")
    for row in cur.fetchall():
        print(f"  ID: {row[0]}, Name: {row[1]}, District: {row[2]}")
        print(f"  Trades ({len(row[3])}): {row[3]}")
    
    cur.close()
    conn.close()
    
    print(f"\n✅ Successfully reloaded {schools_added} schools to production database")

if __name__ == "__main__":
    reload_schools()
