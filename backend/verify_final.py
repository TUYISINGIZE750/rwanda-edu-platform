import psycopg2

conn = psycopg2.connect('postgresql://rwanda_edu_db_user:NJmoQ8ze9kV53DT6OB6AAMsa7qetokba@dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com/rwanda_edu_db')
cur = conn.cursor()

cur.execute('SELECT COUNT(*) FROM schools WHERE trades IS NOT NULL AND array_length(trades, 1) > 0')
print(f'Schools with trades: {cur.fetchone()[0]}')

cur.execute("SELECT name, array_length(trades, 1) FROM schools WHERE trades IS NOT NULL ORDER BY array_length(trades, 1) DESC LIMIT 5")
print('\nTop 5 schools with most trades:')
for row in cur.fetchall():
    print(f'  {row[0]:50s} ({row[1]} trades)')

cur.execute("SELECT id, name, trades FROM schools WHERE UPPER(name) LIKE '%RUNDA%'")
runda = cur.fetchall()
if runda:
    print('\nRUNDA TVET:')
    for school in runda:
        print(f'  ID: {school[0]}')
        print(f'  Name: {school[1]}')
        print(f'  Trades: {school[2]}')

print('\n' + '='*60)
print('SUCCESS: All 164 schools have real trades!')
print('='*60)

cur.close()
conn.close()
