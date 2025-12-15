import json
import http.server
import socketserver
import webbrowser
import threading
import time

def test_locations_data():
    """Test if locations.json is properly formatted and complete"""
    try:
        with open('locations.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Count all levels
        provinces = len(data['provinces'])
        districts = sum(len(p['districts']) for p in data['provinces'])
        sectors = sum(len(d['sectors']) for p in data['provinces'] for d in p['districts'])
        cells = sum(len(s['cells']) for p in data['provinces'] for d in p['districts'] for s in d['sectors'])
        villages = sum(len(c['villages']) for p in data['provinces'] for d in p['districts'] for s in d['sectors'] for c in s['cells'])
        
        print("✅ LOCATIONS DATA VALIDATION")
        print(f"📍 Provinces: {provinces}")
        print(f"📍 Districts: {districts}")
        print(f"📍 Sectors: {sectors}")
        print(f"📍 Cells: {cells}")
        print(f"📍 Villages: {villages}")
        
        # Test first few entries
        print("\n🔍 SAMPLE DATA:")
        first_province = data['provinces'][0]
        print(f"Province: {first_province['name']}")
        
        first_district = first_province['districts'][0]
        print(f"  District: {first_district['name']}")
        
        first_sector = first_district['sectors'][0]
        print(f"    Sector: {first_sector['name']}")
        
        first_cell = first_sector['cells'][0]
        print(f"      Cell: {first_cell['name']}")
        
        first_village = first_cell['villages'][0]
        print(f"        Village: {first_village['name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error validating locations data: {e}")
        return False

def start_server():
    """Start local server to test the registration form"""
    PORT = 8080
    
    class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
    
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"🌐 Server running at http://localhost:{PORT}")
            print(f"📝 Registration form: http://localhost:{PORT}/register.html")
            print("Press Ctrl+C to stop the server")
            
            # Open browser automatically
            def open_browser():
                time.sleep(1)
                webbrowser.open(f'http://localhost:{PORT}/register.html')
            
            threading.Thread(target=open_browser, daemon=True).start()
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    print("🇷🇼 RWANDA REGISTRATION FORM TEST")
    print("=" * 40)
    
    # Test locations data
    if test_locations_data():
        print("\n✅ Locations data is valid!")
        print("\n🚀 Starting local server to test registration form...")
        start_server()
    else:
        print("\n❌ Please fix locations.json file first")