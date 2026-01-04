import psycopg2

conn = psycopg2.connect('postgresql://rwanda_edu_db_user:NJmoQ8ze9kV53DT6OB6AAMsa7qetokba@dpg-d57rkov5r7bs738b03pg-a.oregon-postgres.render.com/rwanda_edu_db')
cur = conn.cursor()

# Get first valid school
cur.execute('SELECT id, name FROM schools ORDER BY id LIMIT 1')
school = cur.fetchone()

if school:
    school_id, school_name = school
    print(f'Using school: {school_name} (ID: {school_id})')
    
    # Fix all users with invalid school_ids
    cur.execute('''
        UPDATE users 
        SET school_id = %s 
        WHERE school_id IS NULL 
           OR school_id NOT IN (SELECT id FROM schools)
    ''', (school_id,))
    
    conn.commit()
    print(f'Fixed {cur.rowcount} users')
else:
    print('No schools found!')

cur.close()
conn.close()
