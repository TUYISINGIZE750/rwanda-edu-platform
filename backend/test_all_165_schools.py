"""Comprehensive test of all 165 schools across all districts"""
import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print("=" * 80)
print("TESTING ALL 165 SCHOOLS - COMPLETE VERIFICATION")
print("=" * 80)

# Get all districts with schools
cursor.execute('''
    SELECT province, district, COUNT(*) as school_count
    FROM schools
    GROUP BY province, district
    ORDER BY province, district
''')

districts = cursor.fetchall()
total_schools = 0
districts_with_schools = 0
districts_without_trades = 0

print("\nALL DISTRICTS WITH SCHOOLS:\n")

for province, district, count in districts:
    total_schools += count
    districts_with_schools += 1
    
    # Check if schools have trades
    cursor.execute('''
        SELECT COUNT(*) FROM schools 
        WHERE province = ? AND district = ? 
        AND (trades IS NULL OR trades = '')
    ''', (province, district))
    
    no_trades = cursor.fetchone()[0]
    
    status = "[OK]" if no_trades == 0 else "[WARNING]"
    print(f"{status} {province:15} / {district:20} : {count:2} schools")
    
    if no_trades > 0:
        districts_without_trades += 1
        print(f"      ^ {no_trades} schools missing trades")

# Get sample schools from each province
print("\n" + "=" * 80)
print("SAMPLE SCHOOLS FROM EACH PROVINCE (with trades):")
print("=" * 80)

for province in ['East', 'Kigali city', 'North', 'South', 'West']:
    cursor.execute('''
        SELECT name, district, trades 
        FROM schools 
        WHERE province = ? AND trades IS NOT NULL AND trades != ''
        LIMIT 2
    ''', (province,))
    
    print(f"\n{province}:")
    for name, district, trades in cursor.fetchall():
        trades_list = trades.split(',')[:3]
        print(f"  - {name[:45]:45} ({district})")
        print(f"    Trades: {', '.join(trades_list)}{'...' if len(trades.split(',')) > 3 else ''}")

# Summary
print("\n" + "=" * 80)
print("FINAL SUMMARY")
print("=" * 80)
print(f"Total Schools in Database: {total_schools}")
print(f"Total Districts: {districts_with_schools}")
print(f"Districts with all schools having trades: {districts_with_schools - districts_without_trades}")

# Check if any schools are missing trades
cursor.execute("SELECT COUNT(*) FROM schools WHERE trades IS NULL OR trades = ''")
missing_trades = cursor.fetchone()[0]

print(f"\nSchools with trades: {total_schools - missing_trades}")
print(f"Schools missing trades: {missing_trades}")

if total_schools == 165 and missing_trades == 0:
    print("\n" + "=" * 80)
    print("[SUCCESS] ALL 165 SCHOOLS LOADED WITH TRADES!")
    print("=" * 80)
elif total_schools == 165:
    print("\n" + "=" * 80)
    print(f"[WARNING] All 165 schools loaded but {missing_trades} missing trades")
    print("=" * 80)
else:
    print("\n" + "=" * 80)
    print(f"[INFO] {total_schools} schools loaded (expected 165)")
    print("=" * 80)

conn.close()
