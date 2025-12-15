"""Real schools data from Rwanda - REB/TVET/TSS"""

# Real secondary schools across Rwanda (sample from major districts)
RWANDA_SCHOOLS = [
    # Kigali City
    {"id": 1, "name": "Lycée de Kigali", "district": "Gasabo", "province": "Kigali City", "type": "Public"},
    {"id": 2, "name": "GS Kacyiru", "district": "Gasabo", "province": "Kigali City", "type": "Public"},
    {"id": 3, "name": "Ecole Secondaire de Nyarutarama", "district": "Gasabo", "province": "Kigali City", "type": "Public"},
    {"id": 4, "name": "GS Kimironko", "district": "Gasabo", "province": "Kigali City", "type": "Public"},
    {"id": 5, "name": "Lycée Notre Dame de Cîteaux", "district": "Kicukiro", "province": "Kigali City", "type": "Private"},
    
    # Eastern Province
    {"id": 6, "name": "GS Rwamagana", "district": "Rwamagana", "province": "Eastern", "type": "Public"},
    {"id": 7, "name": "Ecole Secondaire de Kayonza", "district": "Kayonza", "province": "Eastern", "type": "Public"},
    {"id": 8, "name": "GS Nyagatare", "district": "Nyagatare", "province": "Eastern", "type": "Public"},
    {"id": 9, "name": "Lycée de Kibungo", "district": "Ngoma", "province": "Eastern", "type": "Public"},
    {"id": 10, "name": "GS Kirehe", "district": "Kirehe", "province": "Eastern", "type": "Public"},
    
    # Southern Province
    {"id": 11, "name": "Groupe Scolaire Officiel de Butare", "district": "Huye", "province": "Southern", "type": "Public"},
    {"id": 12, "name": "Lycée de Nyanza", "district": "Nyanza", "province": "Southern", "type": "Public"},
    {"id": 13, "name": "GS Muhanga", "district": "Muhanga", "province": "Southern", "type": "Public"},
    {"id": 14, "name": "Ecole Secondaire de Kamonyi", "district": "Kamonyi", "province": "Southern", "type": "Public"},
    {"id": 15, "name": "GS Ruhango", "district": "Ruhango", "province": "Southern", "type": "Public"},
    
    # Western Province
    {"id": 16, "name": "GS Rubavu", "district": "Rubavu", "province": "Western", "type": "Public"},
    {"id": 17, "name": "Lycée de Gisenyi", "district": "Rubavu", "province": "Western", "type": "Public"},
    {"id": 18, "name": "GS Rusizi", "district": "Rusizi", "province": "Western", "type": "Public"},
    {"id": 19, "name": "Ecole Secondaire de Karongi", "district": "Karongi", "province": "Western", "type": "Public"},
    {"id": 20, "name": "GS Rutsiro", "district": "Rutsiro", "province": "Western", "type": "Public"},
    
    # Northern Province
    {"id": 21, "name": "GS Musanze", "district": "Musanze", "province": "Northern", "type": "Public"},
    {"id": 22, "name": "Lycée de Ruhengeri", "district": "Musanze", "province": "Northern", "type": "Public"},
    {"id": 23, "name": "GS Burera", "district": "Burera", "province": "Northern", "type": "Public"},
    {"id": 24, "name": "Ecole Secondaire de Gicumbi", "district": "Gicumbi", "province": "Northern", "type": "Public"},
    {"id": 25, "name": "GS Gakenke", "district": "Gakenke", "province": "Northern", "type": "Public"},
    
    # Additional Major Schools
    {"id": 26, "name": "Ecole Belge", "district": "Kicukiro", "province": "Kigali City", "type": "Private"},
    {"id": 27, "name": "Green Hills Academy", "district": "Gasabo", "province": "Kigali City", "type": "Private"},
    {"id": 28, "name": "King David Academy", "district": "Gasabo", "province": "Kigali City", "type": "Private"},
    {"id": 29, "name": "Riviera High School", "district": "Gasabo", "province": "Kigali City", "type": "Private"},
    {"id": 30, "name": "Lycée de Nyabihu", "district": "Nyabihu", "province": "Western", "type": "Public"},
]

# TVET Schools
TVET_SCHOOLS = [
    {"id": 31, "name": "IPRC Kigali", "district": "Gasabo", "province": "Kigali City", "type": "TVET"},
    {"id": 32, "name": "IPRC Huye", "district": "Huye", "province": "Southern", "type": "TVET"},
    {"id": 33, "name": "IPRC Musanze", "district": "Musanze", "province": "Northern", "type": "TVET"},
    {"id": 34, "name": "IPRC Ngoma", "district": "Ngoma", "province": "Eastern", "type": "TVET"},
    {"id": 35, "name": "IPRC Karongi", "district": "Karongi", "province": "Western", "type": "TVET"},
]

# TSS Schools (Teacher Training)
TSS_SCHOOLS = [
    {"id": 36, "name": "TSS Rubengera", "district": "Karongi", "province": "Western", "type": "TSS"},
    {"id": 37, "name": "TSS Murunda", "district": "Rwamagana", "province": "Eastern", "type": "TSS"},
    {"id": 38, "name": "TSS Byimana", "district": "Ruhango", "province": "Southern", "type": "TSS"},
]

# Combine all schools
ALL_SCHOOLS = RWANDA_SCHOOLS + TVET_SCHOOLS + TSS_SCHOOLS

# Total: 38 schools across all 5 provinces
