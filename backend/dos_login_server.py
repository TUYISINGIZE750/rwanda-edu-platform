from flask import Flask, request, jsonify, render_template_string
import sqlite3
import hashlib
import os

app = Flask(__name__)

def verify_dos_login(username, password):
    """Verify DOS login credentials"""
    try:
        conn = sqlite3.connect('education_platform.db')
        cursor = conn.cursor()
        
        # Hash the provided password
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
        # Check credentials
        cursor.execute('''
            SELECT id, username, school_name, province, district 
            FROM dos_users 
            WHERE username = ? AND password = ?
        ''', (username, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'success': True,
                'user': {
                    'id': user[0],
                    'username': user[1],
                    'school_name': user[2],
                    'province': user[3],
                    'district': user[4]
                }
            }
        else:
            return {'success': False, 'message': 'Invalid credentials'}
            
    except Exception as e:
        return {'success': False, 'message': f'Database error: {str(e)}'}

@app.route('/')
def home():
    """Serve the DOS login page"""
    try:
        with open('../frontend/dos_login.html', 'r') as f:
            return f.read()
    except:
        return '''
        <h1>DOS Login System</h1>
        <p>Login page not found. Please check the frontend folder.</p>
        <p>Use API endpoint: POST /api/dos-login</p>
        '''

@app.route('/api/dos-login', methods=['POST'])
def dos_login():
    """Handle DOS login API requests"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password required'})
        
        result = verify_dos_login(username, password)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'})

@app.route('/dos-dashboard')
def dos_dashboard():
    """Simple DOS dashboard"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>DOS Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .header { background: #667eea; color: white; padding: 20px; border-radius: 5px; }
            .content { margin-top: 20px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>DOS Dashboard</h1>
            <p>Welcome to the Director of Studies Portal</p>
        </div>
        <div class="content">
            <h2>Dashboard Features:</h2>
            <ul>
                <li>Manage Student Applications</li>
                <li>Review School Programs</li>
                <li>Generate Reports</li>
                <li>Update School Information</li>
            </ul>
            <p><strong>Status:</strong> Login system is working correctly!</p>
        </div>
    </body>
    </html>
    '''

@app.route('/test-credentials')
def test_credentials():
    """Show test credentials"""
    try:
        conn = sqlite3.connect('education_platform.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username, school_name, province FROM dos_users LIMIT 10')
        users = cursor.fetchall()
        conn.close()
        
        html = '<h1>Test DOS Credentials</h1><ul>'
        for i, user in enumerate(users):
            password = f'dos{i+1}2024'
            html += f'<li>Username: {user[0]} | Password: {password} | School: {user[1]}</li>'
        html += '</ul>'
        return html
        
    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    print("Starting DOS Login Server...")
    print("Access the login page at: http://localhost:5000")
    print("Test credentials at: http://localhost:5000/test-credentials")
    app.run(debug=True, host='0.0.0.0', port=5000)