import psycopg2

conn = psycopg2.connect('postgresql://rwanda_edu_db_user:NJmoQ8ze9kV53DT6OB6AAMsa7qetokba@dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com/rwanda_edu_db')
cur = conn.cursor()

cur.execute('SELECT id, name, type FROM groups LIMIT 10')
rows = cur.fetchall()

print('Groups in database:')
for r in rows:
    print(f'  ID: {r[0]}, Name: {r[1]}, Type: {r[2]}')

print(f'\nTotal: {len(rows)} groups')

cur.close()
conn.close()
