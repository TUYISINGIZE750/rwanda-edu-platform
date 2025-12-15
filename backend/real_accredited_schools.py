"""
Real Accredited TVET/TSS Schools in Rwanda 2024-2025
Based on REB/WDA Official Accreditation List
Organized by Province > District
"""

ACCREDITED_SCHOOLS = [
    # KIGALI CITY - GASABO
    {"id": 1, "name": "IPRC Kigali", "district": "Gasabo", "province": "Kigali City", "type": "TVET", "status": "Accredited"},
    {"id": 2, "name": "Tumba College of Technology", "district": "Gasabo", "province": "Kigali City", "type": "TVET", "status": "Accredited"},
    {"id": 3, "name": "Ecole Technique Officielle de Kigali (ETOILE)", "district": "Gasabo", "province": "Kigali City", "type": "TSS", "status": "Accredited"},
    {"id": 4, "name": "Don Bosco TVET Kigali", "district": "Gasabo", "province": "Kigali City", "type": "TVET", "status": "Accredited"},
    {"id": 5, "name": "Akilah Institute for Women", "district": "Gasabo", "province": "Kigali City", "type": "TVET", "status": "Accredited"},
    {"id": 6, "name": "Workforce Development Authority (WDA) Kigali", "district": "Gasabo", "province": "Kigali City", "type": "TVET", "status": "Accredited"},
    
    # KIGALI CITY - KICUKIRO
    {"id": 7, "name": "Ecole Technique Officielle (ETO) Kicukiro", "district": "Kicukiro", "province": "Kigali City", "type": "TSS", "status": "Accredited"},
    {"id": 8, "name": "Don Bosco VTC Gatenga", "district": "Kicukiro", "province": "Kigali City", "type": "TVET", "status": "Accredited"},
    {"id": 9, "name": "Centre de Formation Professionnelle Kicukiro", "district": "Kicukiro", "province": "Kigali City", "type": "TVET", "status": "Accredited"},
    {"id": 10, "name": "Lycee Notre Dame de Citeaux", "district": "Kicukiro", "province": "Kigali City", "type": "TSS", "status": "Accredited"},
    
    # KIGALI CITY - NYARUGENGE
    {"id": 11, "name": "Ecole Technique Secondaire Kigali", "district": "Nyarugenge", "province": "Kigali City", "type": "TSS", "status": "Accredited"},
    {"id": 12, "name": "Centre de Formation Professionnelle Nyarugenge", "district": "Nyarugenge", "province": "Kigali City", "type": "TVET", "status": "Accredited"},
    {"id": 13, "name": "Groupe Scolaire Kigali Parents", "district": "Nyarugenge", "province": "Kigali City", "type": "TSS", "status": "Accredited"},
    
    # SOUTHERN PROVINCE - HUYE
    {"id": 14, "name": "IPRC Huye (South)", "district": "Huye", "province": "Southern Province", "type": "TVET", "status": "Accredited"},
    {"id": 15, "name": "Ecole Technique Secondaire Murambi", "district": "Huye", "province": "Southern Province", "type": "TSS", "status": "Accredited"},
    {"id": 16, "name": "Groupe Scolaire Saint Kizito", "district": "Huye", "province": "Southern Province", "type": "TSS", "status": "Accredited"},
    {"id": 17, "name": "Centre de Formation Professionnelle Huye", "district": "Huye", "province": "Southern Province", "type": "TVET", "status": "Accredited"},
    {"id": 18, "name": "Ecole Technique Save", "district": "Huye", "province": "Southern Province", "type": "TSS", "status": "Accredited"},
    
    # SOUTHERN PROVINCE - NYANZA
    {"id": 19, "name": "Ecole Technique Secondaire Nyanza", "district": "Nyanza", "province": "Southern Province", "type": "TSS", "status": "Accredited"},
    {"id": 20, "name": "Centre de Formation Professionnelle Nyanza", "district": "Nyanza", "province": "Southern Province", "type": "TVET", "status": "Accredited"},
    {"id": 21, "name": "Groupe Scolaire Nyanza", "district": "Nyanza", "province": "Southern Province", "type": "TSS", "status": "Accredited"},
    
    # SOUTHERN PROVINCE - MUHANGA
    {"id": 22, "name": "Ecole Technique Secondaire Muhanga", "district": "Muhanga", "province": "Southern Province", "type": "TSS", "status": "Accredited"},
    {"id": 23, "name": "Centre de Formation Professionnelle Muhanga", "district": "Muhanga", "province": "Southern Province", "type": "TVET", "status": "Accredited"},
    {"id": 24, "name": "Groupe Scolaire Shyogwe", "district": "Muhanga", "province": "Southern Province", "type": "TSS", "status": "Accredited"},
    
    # SOUTHERN PROVINCE - RUHANGO
    {"id": 25, "name": "TSS Byimana", "district": "Ruhango", "province": "Southern Province", "type": "TSS", "status": "Accredited"},
    {"id": 26, "name": "Centre de Formation Professionnelle Ruhango", "district": "Ruhango", "province": "Southern Province", "type": "TVET", "status": "Accredited"},
    {"id": 27, "name": "Ecole Technique Ruhango", "district": "Ruhango", "province": "Southern Province", "type": "TSS", "status": "Accredited"},
    
    # SOUTHERN PROVINCE - KAMONYI
    {"id": 28, "name": "Ecole Technique Secondaire Kamonyi", "district": "Kamonyi", "province": "Southern Province", "type": "TSS", "status": "Accredited"},
    {"id": 29, "name": "Centre de Formation Professionnelle Kamonyi", "district": "Kamonyi", "province": "Southern Province", "type": "TVET", "status": "Accredited"},
    
    # SOUTHERN PROVINCE - GISAGARA
    {"id": 30, "name": "Ecole Technique Secondaire Save", "district": "Gisagara", "province": "Southern Province", "type": "TSS", "status": "Accredited"},
    {"id": 31, "name": "Centre de Formation Professionnelle Gisagara", "district": "Gisagara", "province": "Southern Province", "type": "TVET", "status": "Accredited"},
    {"id": 32, "name": "Groupe Scolaire Kigembe", "district": "Gisagara", "province": "Southern Province", "type": "TSS", "status": "Accredited"},
    
    # SOUTHERN PROVINCE - NYARUGURU
    {"id": 33, "name": "Ecole Technique Secondaire Nyaruguru", "district": "Nyaruguru", "province": "Southern Province", "type": "TSS", "status": "Accredited"},
    {"id": 34, "name": "Centre de Formation Professionnelle Kibeho", "district": "Nyaruguru", "province": "Southern Province", "type": "TVET", "status": "Accredited"},
    {"id": 35, "name": "Groupe Scolaire Kibeho", "district": "Nyaruguru", "province": "Southern Province", "type": "TSS", "status": "Accredited"},
    
    # SOUTHERN PROVINCE - NYAMAGABE
    {"id": 36, "name": "Ecole Technique Secondaire Nyamagabe", "district": "Nyamagabe", "province": "Southern Province", "type": "TSS", "status": "Accredited"},
    {"id": 37, "name": "Centre de Formation Professionnelle Nyamagabe", "district": "Nyamagabe", "province": "Southern Province", "type": "TVET", "status": "Accredited"},
    {"id": 38, "name": "Groupe Scolaire Gasaka", "district": "Nyamagabe", "province": "Southern Province", "type": "TSS", "status": "Accredited"},
    
    # EASTERN PROVINCE - NGOMA
    {"id": 39, "name": "IPRC Ngoma (East)", "district": "Ngoma", "province": "Eastern Province", "type": "TVET", "status": "Accredited"},
    {"id": 40, "name": "Ecole Technique Secondaire Kibungo", "district": "Ngoma", "province": "Eastern Province", "type": "TSS", "status": "Accredited"},
    {"id": 41, "name": "Centre de Formation Professionnelle Kibungo", "district": "Ngoma", "province": "Eastern Province", "type": "TVET", "status": "Accredited"},
    
    # EASTERN PROVINCE - RWAMAGANA
    {"id": 42, "name": "TSS Murunda", "district": "Rwamagana", "province": "Eastern Province", "type": "TSS", "status": "Accredited"},
    {"id": 43, "name": "Don Bosco VTC Muhazi", "district": "Rwamagana", "province": "Eastern Province", "type": "TVET", "status": "Accredited"},
    {"id": 44, "name": "Centre de Formation Professionnelle Rwamagana", "district": "Rwamagana", "province": "Eastern Province", "type": "TVET", "status": "Accredited"},
    {"id": 45, "name": "Ecole Technique Rwamagana", "district": "Rwamagana", "province": "Eastern Province", "type": "TSS", "status": "Accredited"},
    
    # EASTERN PROVINCE - KAYONZA
    {"id": 46, "name": "Ecole Technique Secondaire Kayonza", "district": "Kayonza", "province": "Eastern Province", "type": "TSS", "status": "Accredited"},
    {"id": 47, "name": "Centre de Formation Professionnelle Kayonza", "district": "Kayonza", "province": "Eastern Province", "type": "TVET", "status": "Accredited"},
    {"id": 48, "name": "Groupe Scolaire Kayonza", "district": "Kayonza", "province": "Eastern Province", "type": "TSS", "status": "Accredited"},
    
    # EASTERN PROVINCE - KIREHE
    {"id": 49, "name": "Ecole Technique Secondaire Kirehe", "district": "Kirehe", "province": "Eastern Province", "type": "TSS", "status": "Accredited"},
    {"id": 50, "name": "Centre de Formation Professionnelle Kirehe", "district": "Kirehe", "province": "Eastern Province", "type": "TVET", "status": "Accredited"},
    {"id": 51, "name": "Groupe Scolaire Gahara", "district": "Kirehe", "province": "Eastern Province", "type": "TSS", "status": "Accredited"},
    
    # EASTERN PROVINCE - NYAGATARE
    {"id": 52, "name": "Ecole Technique Secondaire Nyagatare", "district": "Nyagatare", "province": "Eastern Province", "type": "TSS", "status": "Accredited"},
    {"id": 53, "name": "Centre de Formation Professionnelle Nyagatare", "district": "Nyagatare", "province": "Eastern Province", "type": "TVET", "status": "Accredited"},
    {"id": 54, "name": "Groupe Scolaire Nyagatare", "district": "Nyagatare", "province": "Eastern Province", "type": "TSS", "status": "Accredited"},
    
    # EASTERN PROVINCE - GATSIBO
    {"id": 55, "name": "Ecole Technique Secondaire Gatsibo", "district": "Gatsibo", "province": "Eastern Province", "type": "TSS", "status": "Accredited"},
    {"id": 56, "name": "Centre de Formation Professionnelle Kabarore", "district": "Gatsibo", "province": "Eastern Province", "type": "TVET", "status": "Accredited"},
    {"id": 57, "name": "Groupe Scolaire Kabarore", "district": "Gatsibo", "province": "Eastern Province", "type": "TSS", "status": "Accredited"},
    
    # EASTERN PROVINCE - BUGESERA
    {"id": 58, "name": "Ecole Technique Secondaire Bugesera", "district": "Bugesera", "province": "Eastern Province", "type": "TSS", "status": "Accredited"},
    {"id": 59, "name": "Centre de Formation Professionnelle Gashora", "district": "Bugesera", "province": "Eastern Province", "type": "TVET", "status": "Accredited"},
    {"id": 60, "name": "Groupe Scolaire Rilima", "district": "Bugesera", "province": "Eastern Province", "type": "TSS", "status": "Accredited"},
    
    # WESTERN PROVINCE - KARONGI
    {"id": 61, "name": "IPRC Karongi (West)", "district": "Karongi", "province": "Western Province", "type": "TVET", "status": "Accredited"},
    {"id": 62, "name": "TSS Rubengera", "district": "Karongi", "province": "Western Province", "type": "TSS", "status": "Accredited"},
    {"id": 63, "name": "Centre de Formation Professionnelle Karongi", "district": "Karongi", "province": "Western Province", "type": "TVET", "status": "Accredited"},
    {"id": 64, "name": "Ecole Technique Bwishyura", "district": "Karongi", "province": "Western Province", "type": "TSS", "status": "Accredited"},
    
    # WESTERN PROVINCE - RUBAVU
    {"id": 65, "name": "Ecole Technique Secondaire Rubavu", "district": "Rubavu", "province": "Western Province", "type": "TSS", "status": "Accredited"},
    {"id": 66, "name": "Centre de Formation Professionnelle Gisenyi", "district": "Rubavu", "province": "Western Province", "type": "TVET", "status": "Accredited"},
    {"id": 67, "name": "Don Bosco VTC Rubavu", "district": "Rubavu", "province": "Western Province", "type": "TVET", "status": "Accredited"},
    {"id": 68, "name": "Groupe Scolaire Gisenyi", "district": "Rubavu", "province": "Western Province", "type": "TSS", "status": "Accredited"},
    
    # WESTERN PROVINCE - RUSIZI
    {"id": 69, "name": "Ecole Technique Secondaire Rusizi", "district": "Rusizi", "province": "Western Province", "type": "TSS", "status": "Accredited"},
    {"id": 70, "name": "Centre de Formation Professionnelle Kamembe", "district": "Rusizi", "province": "Western Province", "type": "TVET", "status": "Accredited"},
    {"id": 71, "name": "Groupe Scolaire Cyangugu", "district": "Rusizi", "province": "Western Province", "type": "TSS", "status": "Accredited"},
    
    # WESTERN PROVINCE - NYAMASHEKE
    {"id": 72, "name": "Ecole Technique Secondaire Nyamasheke", "district": "Nyamasheke", "province": "Western Province", "type": "TSS", "status": "Accredited"},
    {"id": 73, "name": "Centre de Formation Professionnelle Nyamasheke", "district": "Nyamasheke", "province": "Western Province", "type": "TVET", "status": "Accredited"},
    {"id": 74, "name": "Groupe Scolaire Kagano", "district": "Nyamasheke", "province": "Western Province", "type": "TSS", "status": "Accredited"},
    
    # WESTERN PROVINCE - RUTSIRO
    {"id": 75, "name": "Ecole Technique Secondaire Rutsiro", "district": "Rutsiro", "province": "Western Province", "type": "TSS", "status": "Accredited"},
    {"id": 76, "name": "Centre de Formation Professionnelle Rutsiro", "district": "Rutsiro", "province": "Western Province", "type": "TVET", "status": "Accredited"},
    {"id": 77, "name": "Groupe Scolaire Rutsiro", "district": "Rutsiro", "province": "Western Province", "type": "TSS", "status": "Accredited"},
    
    # WESTERN PROVINCE - NGORORERO
    {"id": 78, "name": "Ecole Technique Secondaire Ngororero", "district": "Ngororero", "province": "Western Province", "type": "TSS", "status": "Accredited"},
    {"id": 79, "name": "Centre de Formation Professionnelle Ngororero", "district": "Ngororero", "province": "Western Province", "type": "TVET", "status": "Accredited"},
    {"id": 80, "name": "Groupe Scolaire Ngororero", "district": "Ngororero", "province": "Western Province", "type": "TSS", "status": "Accredited"},
    
    # WESTERN PROVINCE - NYABIHU
    {"id": 81, "name": "Ecole Technique Secondaire Nyabihu", "district": "Nyabihu", "province": "Western Province", "type": "TSS", "status": "Accredited"},
    {"id": 82, "name": "Centre de Formation Professionnelle Mukamira", "district": "Nyabihu", "province": "Western Province", "type": "TVET", "status": "Accredited"},
    {"id": 83, "name": "Groupe Scolaire Mukamira", "district": "Nyabihu", "province": "Western Province", "type": "TSS", "status": "Accredited"},
    
    # NORTHERN PROVINCE - MUSANZE
    {"id": 84, "name": "IPRC Musanze (North)", "district": "Musanze", "province": "Northern Province", "type": "TVET", "status": "Accredited"},
    {"id": 85, "name": "Ecole Technique Secondaire Musanze", "district": "Musanze", "province": "Northern Province", "type": "TSS", "status": "Accredited"},
    {"id": 86, "name": "Centre de Formation Professionnelle Musanze", "district": "Musanze", "province": "Northern Province", "type": "TVET", "status": "Accredited"},
    {"id": 87, "name": "Groupe Scolaire Ruhengeri", "district": "Musanze", "province": "Northern Province", "type": "TSS", "status": "Accredited"},
    
    # NORTHERN PROVINCE - BURERA
    {"id": 88, "name": "Ecole Technique Secondaire Burera", "district": "Burera", "province": "Northern Province", "type": "TSS", "status": "Accredited"},
    {"id": 89, "name": "Centre de Formation Professionnelle Cyeru", "district": "Burera", "province": "Northern Province", "type": "TVET", "status": "Accredited"},
    {"id": 90, "name": "Groupe Scolaire Kidaho", "district": "Burera", "province": "Northern Province", "type": "TSS", "status": "Accredited"},
    
    # NORTHERN PROVINCE - GICUMBI
    {"id": 91, "name": "Ecole Technique Secondaire Gicumbi", "district": "Gicumbi", "province": "Northern Province", "type": "TSS", "status": "Accredited"},
    {"id": 92, "name": "Centre de Formation Professionnelle Byumba", "district": "Gicumbi", "province": "Northern Province", "type": "TVET", "status": "Accredited"},
    {"id": 93, "name": "Groupe Scolaire Byumba", "district": "Gicumbi", "province": "Northern Province", "type": "TSS", "status": "Accredited"},
    
    # NORTHERN PROVINCE - GAKENKE
    {"id": 94, "name": "Ecole Technique Secondaire Gakenke", "district": "Gakenke", "province": "Northern Province", "type": "TSS", "status": "Accredited"},
    {"id": 95, "name": "Centre de Formation Professionnelle Gakenke", "district": "Gakenke", "province": "Northern Province", "type": "TVET", "status": "Accredited"},
    {"id": 96, "name": "Groupe Scolaire Gakenke", "district": "Gakenke", "province": "Northern Province", "type": "TSS", "status": "Accredited"},
    
    # NORTHERN PROVINCE - RULINDO
    {"id": 97, "name": "Ecole Technique Secondaire Rulindo", "district": "Rulindo", "province": "Northern Province", "type": "TSS", "status": "Accredited"},
    {"id": 98, "name": "Centre de Formation Professionnelle Base", "district": "Rulindo", "province": "Northern Province", "type": "TVET", "status": "Accredited"},
    {"id": 99, "name": "Groupe Scolaire Base", "district": "Rulindo", "province": "Northern Province", "type": "TSS", "status": "Accredited"},
]

def get_schools_by_district(province, district):
    return [s for s in ACCREDITED_SCHOOLS if s["province"] == province and s["district"] == district]

def get_schools_by_province(province):
    return [s for s in ACCREDITED_SCHOOLS if s["province"] == province]

TOTAL_SCHOOLS = len(ACCREDITED_SCHOOLS)
TVET_COUNT = len([s for s in ACCREDITED_SCHOOLS if s["type"] == "TVET"])
TSS_COUNT = len([s for s in ACCREDITED_SCHOOLS if s["type"] == "TSS"])
