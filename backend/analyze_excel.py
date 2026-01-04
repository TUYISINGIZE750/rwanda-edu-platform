import pandas as pd

# Read Excel
df = pd.read_excel('10__3__22_UPDATED_LIST_OF_TVET_SCHOOLS_AND_TRADES_TO_BE_CHOSEN_BY_S3_CANDIDATES__2022_1_.xlsx', skiprows=1)

print("="*70)
print("DEEP ANALYSIS OF TVET SCHOOLS EXCEL FILE")
print("="*70)

# Total rows
print(f"\nTotal rows in Excel: {len(df)}")

# Unique schools
schools = df['School Name '].dropna().unique()
print(f"Total unique schools: {len(schools)}")

# Group by school and count trades
school_trades = df.groupby('School Name ')['Trade in full'].apply(list).to_dict()

print(f"\n{'='*70}")
print("ALL SCHOOLS WITH TRADE COUNTS:")
print("="*70)

for i, (school, trades) in enumerate(sorted(school_trades.items()), 1):
    print(f"{i:3d}. {school:50s} ({len(trades)} trades)")

print(f"\n{'='*70}")
print("SAMPLE SCHOOLS WITH FULL DETAILS:")
print("="*70)

# Show first 5 and RUNDA
for school in list(sorted(school_trades.keys()))[:5]:
    print(f"\n{school}:")
    print(f"  Trades: {', '.join(school_trades[school])}")

# Find RUNDA
runda_schools = [s for s in school_trades.keys() if 'RUNDA' in s.upper()]
if runda_schools:
    print(f"\n{'='*70}")
    for school in runda_schools:
        print(f"\n{school}:")
        print(f"  Trades: {', '.join(school_trades[school])}")

print(f"\n{'='*70}")
print(f"SUMMARY: {len(schools)} unique TVET schools found in Excel")
print("="*70)
