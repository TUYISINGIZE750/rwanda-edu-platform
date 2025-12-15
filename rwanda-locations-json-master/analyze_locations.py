import json

def analyze_rwanda_locations():
    with open('locations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Count all administrative levels
    provinces = len(data['provinces'])
    districts = sum(len(p['districts']) for p in data['provinces'])
    sectors = sum(len(d['sectors']) for p in data['provinces'] for d in p['districts'])
    cells = sum(len(s['cells']) for p in data['provinces'] for d in p['districts'] for s in d['sectors'])
    villages = sum(len(c['villages']) for p in data['provinces'] for d in p['districts'] for s in d['sectors'] for c in s['cells'])
    
    print(f"🇷🇼 RWANDA COMPLETE ADMINISTRATIVE STRUCTURE")
    print(f"=" * 50)
    print(f"📍 Provinces: {provinces}")
    print(f"📍 Districts: {districts}")
    print(f"📍 Sectors: {sectors}")
    print(f"📍 Cells: {cells}")
    print(f"📍 Villages: {villages}")
    print(f"📍 Total Lines: {villages + cells + sectors + districts + provinces}")
    
    # List all provinces and their districts
    print(f"\n📋 COMPLETE STRUCTURE:")
    for i, province in enumerate(data['provinces'], 1):
        print(f"\n{i}. PROVINCE: {province['name']}")
        for j, district in enumerate(province['districts'], 1):
            print(f"   {i}.{j} District: {district['name']} ({len(district['sectors'])} sectors)")
    
    return data

def search_location(data, term):
    results = []
    for province in data['provinces']:
        for district in province['districts']:
            for sector in district['sectors']:
                for cell in sector['cells']:
                    for village in cell['villages']:
                        if term.lower() in village['name'].lower():
                            results.append({
                                'village': village['name'],
                                'cell': cell['name'],
                                'sector': sector['name'],
                                'district': district['name'],
                                'province': province['name']
                            })
    return results

def get_province_data(data, province_name):
    for province in data['provinces']:
        if province_name.lower() in province['name'].lower():
            return province
    return None

if __name__ == "__main__":
    data = analyze_rwanda_locations()
    
    # Example searches
    print(f"\n🔍 Search example - Villages with 'Kigali':")
    results = search_location(data, "Kigali")[:3]
    for r in results:
        print(f"   {r['village']} → {r['cell']} → {r['sector']} → {r['district']} → {r['province']}")