import psycopg2

conn = psycopg2.connect('postgresql://rwanda_edu_db_user:NJmoQ8ze9kV53DT6OB6AAMsa7qetokba@dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com/rwanda_edu_db')
cur = conn.cursor()

# Check teachers
cur.execute("SELECT id, email, school_id FROM users WHERE role = 'TEACHER' LIMIT 5")
print('Teachers:')
for row in cur.fetchall():
    print(f'  ID: {row[0]}, Email: {row[1]}, School: {row[2]}')

# Check schools
cur.execute('SELECT id, name FROM schools ORDER BY id LIMIT 10')
print('\nSchools:')
for row in cur.fetchall():
    print(f'  ID: {row[0]}, Name: {row[1]}')

# Find RUNDA
cur.execute("SELECT id, name FROM schools WHERE UPPER(name) LIKE '%RUNDA%'")
runda = cur.fetchall()
if runda:
    print(f'\nRUNDA TVET: ID = {runda[0][0]}')
    
    # Update teacher to use RUNDA school
    cur.execute("UPDATE users SET school_id = %s WHERE role = 'TEACHER'", (runda[0][0],))
    conn.commit()
    print(f'Updated all teachers to school_id = {runda[0][0]}')

cur.close()
conn.close()
