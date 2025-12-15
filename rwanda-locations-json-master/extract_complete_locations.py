import json
import os

def extract_complete_locations():
    # Read the original locations.json file
    input_file = "locations.json"
    output_file = "rwanda_complete_locations.json"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Count statistics
        stats = {
            'provinces': len(data['provinces']),
            'districts': 0,
            'sectors': 0,
            'cells': 0,
            'villages': 0
        }
        
        # Count all administrative levels
        for province in data['provinces']:
            stats['districts'] += len(province['districts'])
            for district in province['districts']:
                stats['sectors'] += len(district['sectors'])
                for sector in district['sectors']:
                    stats['cells'] += len(sector['cells'])
                    for cell in sector['cells']:
                        stats['villages'] += len(cell['villages'])
        
        # Create complete structure with all data
        complete_data = {
            "metadata": {
                "country": "Rwanda",
                "total_provinces": stats['provinces'],
                "total_districts": stats['districts'],
                "total_sectors": stats['sectors'],
                "total_cells": stats['cells'],
                "total_villages": stats['villages'],
                "generated_date": "2024"
            },
            "provinces": data['provinces']
        }
        
        # Write complete data to new file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(complete_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Complete Rwanda locations extracted successfully!")
        print(f"📊 Statistics:")
        print(f"   - Provinces: {stats['provinces']}")
        print(f"   - Districts: {stats['districts']}")
        print(f"   - Sectors: {stats['sectors']}")
        print(f"   - Cells: {stats['cells']}")
        print(f"   - Villages: {stats['villages']}")
        print(f"📁 Output file: {output_file}")
        
        return complete_data
        
    except FileNotFoundError:
        print(f"❌ Error: {input_file} not found!")
        return None
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in {input_file}")
        return None

def search_location(data, search_term):
    """Search for a location across all levels"""
    results = []
    
    for province in data['provinces']:
        if search_term.lower() in province['name'].lower():
            results.append(f"Province: {province['name']}")
            
        for district in province['districts']:
            if search_term.lower() in district['name'].lower():
                results.append(f"District: {district['name']} (Province: {province['name']})")
                
            for sector in district['sectors']:
                if search_term.lower() in sector['name'].lower():
                    results.append(f"Sector: {sector['name']} (District: {district['name']}, Province: {province['name']})")
                    
                for cell in sector['cells']:
                    if search_term.lower() in cell['name'].lower():
                        results.append(f"Cell: {cell['name']} (Sector: {sector['name']}, District: {district['name']}, Province: {province['name']})")
                        
                    for village in cell['villages']:
                        if search_term.lower() in village['name'].lower():
                            results.append(f"Village: {village['name']} (Cell: {cell['name']}, Sector: {sector['name']}, District: {district['name']}, Province: {province['name']})")
    
    return results

if __name__ == "__main__":
    # Extract complete locations
    complete_data = extract_complete_locations()
    
    if complete_data:
        # Example search
        print("\n🔍 Example search for 'Kigali':")
        results = search_location(complete_data, "Kigali")
        for result in results[:5]:  # Show first 5 results
            print(f"   {result}")
        
        print(f"\n✅ Complete! All {complete_data['metadata']['total_villages']} villages from all {complete_data['metadata']['total_provinces']} provinces are now available.")