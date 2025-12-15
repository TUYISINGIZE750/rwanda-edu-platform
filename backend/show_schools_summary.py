import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print("=" * 70)
print("SCHOOLS DATABASE SUMMARY")
print("=" * 70)

# Total schools
cursor.execute('SELECT COUNT(*) FROM schools')
total = cursor.fetchone()[0]
print(f"\nTotal Schools: {total}")

# Schools by province
print("\n" + "-" * 70)
print("SCHOOLS BY PROVINCE:")
print("-" * 70)
cursor.execute('SELECT province, COUNT(*) FROM schools GROUP BY province ORDER BY province')
for row in cursor.fetchall():
    print(f"{row[0]:20} : {row[1]:3} schools")

# Schools by district
print("\n" + "-" * 70)
print("SCHOOLS BY DISTRICT:")
print("-" * 70)
cursor.execute('SELECT province, district, COUNT(*) FROM schools GROUP BY province, district ORDER BY province, district')
current_province = ''
for row in cursor.fetchall():
    if row[0] != current_province:
        print(f"\n{row[0]}:")
        current_province = row[0]
    print(f"  {row[1]:20} : {row[2]:2} schools")

# Sample schools with trades
print("\n" + "-" * 70)
print("SAMPLE SCHOOLS WITH TRADES:")
print("-" * 70)
cursor.execute('SELECT name, district, trades FROM schools LIMIT 5')
for row in cursor.fetchall():
    trades_list = row[2].split(',') if row[2] else []
    print(f"\n{row[0]} ({row[1]})")
    print(f"  Trades: {', '.join(trades_list[:3])}{'...' if len(trades_list) > 3 else ''}")

conn.close()

print("\n" + "=" * 70)
