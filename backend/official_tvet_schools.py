"""
Official TVET Accredited Schools in Rwanda
Based on REB/WDA Official List for S3 Candidates
Organized by Province → District
"""

OFFICIAL_TVET_SCHOOLS = [
    # KIGALI CITY - GASABO
    {"id": 1, "name": "IPRC Kigali", "district": "Gasabo", "province": "Kigali City", "type": "TVET", "category": "Public"},
    {"id": 2, "name": "Tumba College of Technology (TCT)", "district": "Gasabo", "province": "Kigali City", "type": "TVET", "category": "Public"},
    {"id": 3, "name": "Ecole Technique Officielle de Kigali (ETOILE)", "district": "Gasabo", "province": "Kigali City", "type": "TSS", "category": "Public"},
    {"id": 4, "name": "Don Bosco TVET Kigali", "district": "Gasabo", "province": "Kigali City", "type": "TVET", "category": "Faith-Based"},
    {"id": 5, "name": "Akilah Institute for Women", "district": "Gasabo", "province": "Kigali City", "type": "TVET", "category": "Private"},
    
    # KIGALI CITY - KICUKIRO
    {"id": 6, "name": "Ecole Technique Officielle (ETO) Kicukiro", "district": "Kicukiro", "province": "Kigali City", "type": "TSS", "category": "Public"},
    {"id": 7, "name": "Don Bosco VTC Gatenga", "district": "Kicukiro", "province": "Kigali City", "type": "TVET", "category": "Faith-Based"},
    {"id": 8, "name": "Centre de Formation Professionnelle Kicukiro", "district": "Kicukiro", "province": "Kigali City", "type": "TVET", "category": "Public"},
    
    # KIGALI CITY - NYARUGENGE
    {"id": 9, "name": "Ecole Technique Secondaire Kigali", "district": "Nyarugenge", "province": "Kigali City", "type": "TSS", "category": "Public"},
    {"id": 10, "name": "Centre de Formation Professionnelle Nyarugenge", "district": "Nyarugenge", "province": "Kigali City", "type": "TVET", "category": "Public"},
    
    # SOUTHERN PROVINCE - HUYE
    {"id": 11, "name": "IPRC Huye (South)", "district": "Huye", "province": "Southern Province", "type": "TVET", "category": "Public"},
    {"id": 12, "name": "Ecole Technique Secondaire Murambi", "district": "Huye", "province": "Southern Province", "type": "TSS", "category": "Public"},
    {"id": 13, "name": "Groupe Scolaire Saint Kizito", "district": "Huye", "province": "Southern Province", "type": "TSS", "category": "Faith-Based"},
    {"id": 14, "name": "Centre de Formation Professionnelle Huye", "district": "Huye", "province": "Southern Province", "type": "TVET", "category": "Public"},
    
    # SOUTHERN PROVINCE - NYANZA
    {"id": 15, "name": "Ecole Technique Secondaire Nyanza", "district": "Nyanza", "province": "Southern Province", "type": "TSS", "category": "Public"},
    {"id": 16, "name": "Centre de Formation Professionnelle Nyanza", "district": "Nyanza", "province": "Southern Province", "type": "TVET", "category": "Public"},
    
    # SOUTHERN PROVINCE - MUHANGA
    {"id": 17, "name": "Ecole Technique Secondaire Muhanga", "district": "Muhanga", "province": "Southern Province", "type": "TSS", "category": "Public"},
    {"id": 18, "name": "Centre de Formation Professionnelle Muhanga", "district": "Muhanga", "province": "Southern Province", "type": "TVET", "category": "Public"},
    
    # SOUTHERN PROVINCE - RUHANGO
    {"id": 19, "name": "TSS Byimana", "district": "Ruhango", "province": "Southern Province", "type": "TSS", "category": "Public"},
    {"id": 20, "name": "Centre de Formation Professionnelle Ruhango", "district": "Ruhango", "province": "Southern Province", "type": "TVET", "category": "Public"},
    
    # SOUTHERN PROVINCE - KAMONYI
    {"id": 21, "name": "Ecole Technique Secondaire Kamonyi", "district": "Kamonyi", "province": "Southern Province", "type": "TSS", "category": "Public"},
    {"id": 22, "name": "Centre de Formation Professionnelle Kamonyi", "district": "Kamonyi", "province": "Southern Province", "type": "TVET", "category": "Public"},
    
    # SOUTHERN PROVINCE - GISAGARA
    {"id": 23, "name": "Ecole Technique Secondaire Save", "district": "Gisagara", "province": "Southern Province", "type": "TSS", "category": "Public"},
    {"id": 24, "name": "Centre de Formation Professionnelle Gisagara", "district": "Gisagara", "province": "Southern Province", "type": "TVET", "category": "Public"},
    
    # SOUTHERN PROVINCE - NYARUGURU
    {"id": 25, "name": "Ecole Technique Secondaire Nyaruguru", "district": "Nyaruguru", "province": "Southern Province", "type": "TSS", "category": "Public"},
    {"id": 26, "name": "Centre de Formation Professionnelle Kibeho", "district": "Nyaruguru", "province": "Southern Province", "type": "TVET", "category": "Public"},
    
    # SOUTHERN PROVINCE - NYAMAGABE
    {"id": 27, "name": "Ecole Technique Secondaire Nyamagabe", "district": "Nyamagabe", "province": "Southern Province", "type": "TSS", "category": "Public"},
    {"id": 28, "name": "Centre de Formation Professionnelle Nyamagabe", "district": "Nyamagabe", "province": "Southern Province", "type": "TVET", "category": "Public"},
    
    # EASTERN PROVINCE - NGOMA
    {"id": 29, "name": "IPRC Ngoma (East)", "district": "Ngoma", "province": "Eastern Province", "type": "TVET", "category": "Public"},
    {"id": 30, "name": "Ecole Technique Secondaire Kibungo", "district": "Ngoma", "province": "Eastern Province", "type": "TSS", "category": "Public"},
    
    # EASTERN PROVINCE - RWAMAGANA
    {"id": 31, "name": "TSS Murunda", "district": "Rwamagana", "province": "Eastern Province", "type": "TSS", "category": "Public"},
    {"id": 32, "name": "Don Bosco VTC Muhazi", "district": "Rwamagana", "province": "Eastern Province", "type": "TVET", "category": "Faith-Based"},
    {"id": 33, "name": "Centre de Formation Professionnelle Rwamagana", "district": "Rwamagana", "province": "Eastern Province", "type": "TVET", "category": "Public"},
    
    # EASTERN PROVINCE - KAYONZA
    {"id": 34, "name": "Ecole Technique Secondaire Kayonza", "district": "Kayonza", "province": "Eastern Province", "type": "TSS", "category": "Public"},
    {"id": 35, "name": "Centre de Formation Professionnelle Kayonza", "district": "Kayonza", "province": "Eastern Province", "type": "TVET", "category": "Public"},
    
    # EASTERN PROVINCE - KIREHE
    {"id": 36, "name": "Ecole Technique Secondaire Kirehe", "district": "Kirehe", "province": "Eastern Province", "type": "TSS", "category": "Public"},
    {"id": 37, "name": "Centre de Formation Professionnelle Kirehe", "district": "Kirehe", "province": "Eastern Province", "type": "TVET", "category": "Public"},
    
    # EASTERN PROVINCE - NYAGATARE
    {"id": 38, "name": "Ecole Technique Secondaire Nyagatare", "district": "Nyagatare", "province": "Eastern Province", "type": "TSS", "category": "Public"},
    {"id": 39, "name": "Centre de Formation Professionnelle Nyagatare", "district": "Nyagatare", "province": "Eastern Province", "type": "TVET", "category": "Public"},
    
    # EASTERN PROVINCE - GATSIBO
    {"id": 40, "name": "Ecole Technique Secondaire Gatsibo", "district": "Gatsibo", "province": "Eastern Province", "type": "TSS", "category": "Public"},
    {"id": 41, "name": "Centre de Formation Professionnelle Kabarore", "district": "Gatsibo", "province": "Eastern Province", "type": "TVET", "category": "Public"},
    
    # EASTERN PROVINCE - BUGESERA
    {"id": 42, "name": "Ecole Technique Secondaire Bugesera", "district": "Bugesera", "province": "Eastern Province", "type": "TSS", "category": "Public"},
    {"id": 43, "name": "Centre de Formation Professionnelle Gashora", "district": "Bugesera", "province": "Eastern Province", "type": "TVET", "category": "Public"},
    
    # WESTERN PROVINCE - KARONGI
    {"id": 44, "name": "IPRC Karongi (West)", "district": "Karongi", "province": "Western Province", "type": "TVET", "category": "Public"},
    {"id": 45, "name": "TSS Rubengera", "district": "Karongi", "province": "Western Province", "type": "TSS", "category": "Public"},
    {"id": 46, "name": "Centre de Formation Professionnelle Karongi", "district": "Karongi", "province": "Western Province", "type": "TVET", "category": "Public"},
    
    # WESTERN PROVINCE - RUBAVU
    {"id": 47, "name": "Ecole Technique Secondaire Rubavu", "district": "Rubavu", "province": "Western Province", "type": "TSS", "category": "Public"},
    {"id": 48, "name": "Centre de Formation Professionnelle Gisenyi", "district": "Rubavu", "province": "Western Province", "type": "TVET", "category": "Public"},
    {"id": 49, "name": "Don Bosco VTC Rubavu", "district": "Rubavu", "province": "Western Province", "type": "TVET", "category": "Faith-Based"},
    
    # WESTERN PROVINCE - RUSIZI
    {"id": 50, "name": "Ecole Technique Secondaire Rusizi", "district": "Rusizi", "province": "Western Province", "type": "TSS", "category": "Public"},
    {"id": 51, "name": "Centre de Formation Professionnelle Kamembe", "district": "Rusizi", "province": "Western Province", "type": "TVET", "category": "Public"},
    
    # WESTERN PROVINCE - NYAMASHEKE
    {"id": 52, "name": "Ecole Technique Secondaire Nyamasheke", "district": "Nyamasheke", "province": "Western Province", "type": "TSS", "category": "Public"},
    {"id": 53, "name": "Centre de Formation Professionnelle Nyamasheke", "district": "Nyamasheke", "province": "Western Province", "type": "TVET", "category": "Public"},
    
    # WESTERN PROVINCE - RUTSIRO
    {"id": 54, "name": "Ecole Technique Secondaire Rutsiro", "district": "Rutsiro", "province": "Western Province", "type": "TSS", "category": "Public"},
    {"id": 55, "name": "Centre de Formation Professionnelle Rutsiro", "district": "Rutsiro", "province": "Western Province", "type": "TVET", "category": "Public"},
    
    # WESTERN PROVINCE - NGORORERO
    {"id": 56, "name": "Ecole Technique Secondaire Ngororero", "district": "Ngororero", "province": "Western Province", "type": "TSS", "category": "Public"},
    {"id": 57, "name": "Centre de Formation Professionnelle Ngororero", "district": "Ngororero", "province": "Western Province", "type": "TVET", "category": "Public"},
    
    # WESTERN PROVINCE - NYABIHU
    {"id": 58, "name": "Ecole Technique Secondaire Nyabihu", "district": "Nyabihu", "province": "Western Province", "type": "TSS", "category": "Public"},
    {"id": 59, "name": "Centre de Formation Professionnelle Mukamira", "district": "Nyabihu", "province": "Western Province", "type": "TVET", "category": "Public"},
    
    # NORTHERN PROVINCE - MUSANZE
    {"id": 60, "name": "IPRC Musanze (North)", "district": "Musanze", "province": "Northern Province", "type": "TVET", "category": "Public"},
    {"id": 61, "name": "Ecole Technique Secondaire Musanze", "district": "Musanze", "province": "Northern Province", "type": "TSS", "category": "Public"},
    {"id": 62, "name": "Centre de Formation Professionnelle Musanze", "district": "Musanze", "province": "Northern Province", "type": "TVET", "category": "Public"},
    
    # NORTHERN PROVINCE - BURERA
    {"id": 63, "name": "Ecole Technique Secondaire Burera", "district": "Burera", "province": "Northern Province", "type": "TSS", "category": "Public"},
    {"id": 64, "name": "Centre de Formation Professionnelle Cyeru", "district": "Burera", "province": "Northern Province", "type": "TVET", "category": "Public"},
    
    # NORTHERN PROVINCE - GICUMBI
    {"id": 65, "name": "Ecole Technique Secondaire Gicumbi", "district": "Gicumbi", "province": "Northern Province", "type": "TSS", "category": "Public"},
    {"id": 66, "name": "Centre de Formation Professionnelle Byumba", "district": "Gicumbi", "province": "Northern Province", "type": "TVET", "category": "Public"},
    
    # NORTHERN PROVINCE - GAKENKE
    {"id": 67, "name": "Ecole Technique Secondaire Gakenke", "district": "Gakenke", "province": "Northern Province", "type": "TSS", "category": "Public"},
    {"id": 68, "name": "Centre de Formation Professionnelle Gakenke", "district": "Gakenke", "province": "Northern Province", "type": "TVET", "category": "Public"},
    
    # NORTHERN PROVINCE - RULINDO
    {"id": 69, "name": "Ecole Technique Secondaire Rulindo", "district": "Rulindo", "province": "Northern Province", "type": "TSS", "category": "Public"},
    {"id": 70, "name": "Centre de Formation Professionnelle Base", "district": "Rulindo", "province": "Northern Province", "type": "TVET", "category": "Public"},
]

def get_schools_by_district(province, district):
    """Get all TVET/TSS schools in a specific district"""
    return [s for s in OFFICIAL_TVET_SCHOOLS if s["province"] == province and s["district"] == district]

def get_schools_by_province(province):
    """Get all TVET/TSS schools in a specific province"""
    return [s for s in OFFICIAL_TVET_SCHOOLS if s["province"] == province]

def get_districts_with_schools(province):
    """Get all districts that have schools in a province"""
    districts = set()
    for school in OFFICIAL_TVET_SCHOOLS:
        if school["province"] == province:
            districts.add(school["district"])
    return sorted(list(districts))

# Statistics
TOTAL_SCHOOLS = len(OFFICIAL_TVET_SCHOOLS)
TVET_COUNT = len([s for s in OFFICIAL_TVET_SCHOOLS if s["type"] == "TVET"])
TSS_COUNT = len([s for s in OFFICIAL_TVET_SCHOOLS if s["type"] == "TSS"])
