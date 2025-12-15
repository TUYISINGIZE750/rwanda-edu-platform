import json

def generate_full_register():
    # Read the complete locations.json
    with open('locations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convert to JavaScript format
    js_data = json.dumps(data, indent=8)
    
    # HTML template with embedded data
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rwanda Registration Form - Complete</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }}
        .form-group {{ margin-bottom: 15px; }}
        label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
        select, input {{ width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }}
        button {{ background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }}
        button:hover {{ background: #0056b3; }}
        .stats {{ background: #f8f9fa; padding: 15px; border-radius: 4px; margin-bottom: 20px; }}
        .loading {{ color: #666; }}
    </style>
</head>
<body>
    <div class="stats">
        <h3>🇷🇼 Rwanda Registration Form</h3>
        <p id="stats" class="loading">Loading complete Rwanda data...</p>
    </div>
    
    <form id="registrationForm">
        <div class="form-group">
            <label for="fullName">Full Name:</label>
            <input type="text" id="fullName" name="fullName" required>
        </div>

        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>

        <div class="form-group">
            <label for="phone">Phone Number:</label>
            <input type="tel" id="phone" name="phone" required>
        </div>

        <div class="form-group">
            <label for="province">Province:</label>
            <select id="province" name="province" required>
                <option value="">Select Province</option>
            </select>
        </div>

        <div class="form-group">
            <label for="district">District:</label>
            <select id="district" name="district" required disabled>
                <option value="">Select District</option>
            </select>
        </div>

        <div class="form-group">
            <label for="sector">Sector:</label>
            <select id="sector" name="sector" required disabled>
                <option value="">Select Sector</option>
            </select>
        </div>

        <div class="form-group">
            <label for="cell">Cell:</label>
            <select id="cell" name="cell" required disabled>
                <option value="">Select Cell</option>
            </select>
        </div>

        <div class="form-group">
            <label for="village">Village:</label>
            <select id="village" name="village" required disabled>
                <option value="">Select Village</option>
            </select>
        </div>

        <button type="submit">Register</button>
    </form>

    <script>
        // Complete Rwanda locations data
        const rwandaData = {js_data};

        // Count statistics
        function countStats() {{
            let provinces = rwandaData.provinces.length;
            let districts = 0, sectors = 0, cells = 0, villages = 0;
            
            rwandaData.provinces.forEach(province => {{
                districts += province.districts.length;
                province.districts.forEach(district => {{
                    sectors += district.sectors.length;
                    district.sectors.forEach(sector => {{
                        cells += sector.cells.length;
                        sector.cells.forEach(cell => {{
                            villages += cell.villages.length;
                        }});
                    }});
                }});
            }});
            
            return {{ provinces, districts, sectors, cells, villages }};
        }}

        // Initialize form
        function initializeForm() {{
            const stats = countStats();
            document.getElementById('stats').innerHTML = 
                `✅ <strong>Complete Rwanda Data Loaded:</strong><br>
                📍 ${{stats.provinces}} Provinces | ${{stats.districts}} Districts | ${{stats.sectors}} Sectors | ${{stats.cells}} Cells | ${{stats.villages}} Villages`;
            
            populateProvinces();
        }}

        // Populate provinces
        function populateProvinces() {{
            const provinceSelect = document.getElementById('province');
            provinceSelect.innerHTML = '<option value="">Select Province</option>';
            
            rwandaData.provinces.forEach(province => {{
                const option = document.createElement('option');
                option.value = province.name;
                option.textContent = province.name;
                provinceSelect.appendChild(option);
            }});
        }}

        // Populate districts
        function populateDistricts(provinceName) {{
            const districtSelect = document.getElementById('district');
            const sectorSelect = document.getElementById('sector');
            const cellSelect = document.getElementById('cell');
            const villageSelect = document.getElementById('village');
            
            districtSelect.innerHTML = '<option value="">Select District</option>';
            sectorSelect.innerHTML = '<option value="">Select Sector</option>';
            cellSelect.innerHTML = '<option value="">Select Cell</option>';
            villageSelect.innerHTML = '<option value="">Select Village</option>';
            
            districtSelect.disabled = false;
            sectorSelect.disabled = true;
            cellSelect.disabled = true;
            villageSelect.disabled = true;

            const province = rwandaData.provinces.find(p => p.name === provinceName);
            if (province) {{
                province.districts.forEach(district => {{
                    const option = document.createElement('option');
                    option.value = district.name;
                    option.textContent = district.name;
                    districtSelect.appendChild(option);
                }});
            }}
        }}

        // Populate sectors
        function populateSectors(provinceName, districtName) {{
            const sectorSelect = document.getElementById('sector');
            const cellSelect = document.getElementById('cell');
            const villageSelect = document.getElementById('village');
            
            sectorSelect.innerHTML = '<option value="">Select Sector</option>';
            cellSelect.innerHTML = '<option value="">Select Cell</option>';
            villageSelect.innerHTML = '<option value="">Select Village</option>';
            
            sectorSelect.disabled = false;
            cellSelect.disabled = true;
            villageSelect.disabled = true;

            const province = rwandaData.provinces.find(p => p.name === provinceName);
            const district = province?.districts.find(d => d.name === districtName);
            
            if (district) {{
                district.sectors.forEach(sector => {{
                    const option = document.createElement('option');
                    option.value = sector.name;
                    option.textContent = sector.name;
                    sectorSelect.appendChild(option);
                }});
            }}
        }}

        // Populate cells
        function populateCells(provinceName, districtName, sectorName) {{
            const cellSelect = document.getElementById('cell');
            const villageSelect = document.getElementById('village');
            
            cellSelect.innerHTML = '<option value="">Select Cell</option>';
            villageSelect.innerHTML = '<option value="">Select Village</option>';
            
            cellSelect.disabled = false;
            villageSelect.disabled = true;

            const province = rwandaData.provinces.find(p => p.name === provinceName);
            const district = province?.districts.find(d => d.name === districtName);
            const sector = district?.sectors.find(s => s.name === sectorName);
            
            if (sector) {{
                sector.cells.forEach(cell => {{
                    const option = document.createElement('option');
                    option.value = cell.name;
                    option.textContent = cell.name;
                    cellSelect.appendChild(option);
                }});
            }}
        }}

        // Populate villages
        function populateVillages(provinceName, districtName, sectorName, cellName) {{
            const villageSelect = document.getElementById('village');
            
            villageSelect.innerHTML = '<option value="">Select Village</option>';
            villageSelect.disabled = false;

            const province = rwandaData.provinces.find(p => p.name === provinceName);
            const district = province?.districts.find(d => d.name === districtName);
            const sector = district?.sectors.find(s => s.name === sectorName);
            const cell = sector?.cells.find(c => c.name === cellName);
            
            if (cell) {{
                cell.villages.forEach(village => {{
                    const option = document.createElement('option');
                    option.value = village.name;
                    option.textContent = village.name;
                    villageSelect.appendChild(option);
                }});
            }}
        }}

        // Event listeners
        document.getElementById('province').addEventListener('change', function() {{
            if (this.value) populateDistricts(this.value);
        }});

        document.getElementById('district').addEventListener('change', function() {{
            const province = document.getElementById('province').value;
            if (this.value && province) populateSectors(province, this.value);
        }});

        document.getElementById('sector').addEventListener('change', function() {{
            const province = document.getElementById('province').value;
            const district = document.getElementById('district').value;
            if (this.value && province && district) populateCells(province, district, this.value);
        }});

        document.getElementById('cell').addEventListener('change', function() {{
            const province = document.getElementById('province').value;
            const district = document.getElementById('district').value;
            const sector = document.getElementById('sector').value;
            if (this.value && province && district && sector) populateVillages(province, district, sector, this.value);
        }});

        // Form submission
        document.getElementById('registrationForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            alert(`✅ Registration Successful!\\n\\nName: ${{data.fullName}}\\nEmail: ${{data.email}}\\nPhone: ${{data.phone}}\\nLocation: ${{data.village}}, ${{data.cell}}, ${{data.sector}}, ${{data.district}}, ${{data.province}}`);
        }});

        // Initialize on load
        window.addEventListener('load', initializeForm);
    </script>
</body>
</html>'''

    # Write the complete HTML file
    with open('rwanda_complete_register.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Complete registration form generated!")
    print("📁 File: rwanda_complete_register.html")
    print("🎯 Double-click to open - contains all Rwanda locations!")

if __name__ == "__main__":
    generate_full_register()