from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Rwanda Education Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/v1/locations/provinces")
def provinces():
    return [
        {"name": "Kigali City"},
        {"name": "Southern Province"},
        {"name": "Western Province"},
        {"name": "Northern Province"},
        {"name": "Eastern Province"}
    ]

@app.get("/api/v1/locations/districts/{province_name}")
def districts(province_name: str):
    data = {
        "Kigali City": ["Gasabo", "Kicukiro", "Nyarugenge"],
        "Southern Province": ["Kamonyi", "Muhanga", "Ruhango", "Nyanza", "Huye"],
        "Western Province": ["Karongi", "Rutsiro", "Rubavu", "Nyabihu"],
        "Northern Province": ["Rulindo", "Gakenke", "Musanze", "Burera"],
        "Eastern Province": ["Rwamagana", "Nyagatare", "Gatsibo", "Kayonza"]
    }
    return [{"name": d} for d in data.get(province_name, [])]

@app.get("/api/v1/locations/schools/district/{province_name}/{district_name}")
def schools(province_name: str, district_name: str):
    return [
        {"id": 1, "name": f"{district_name} Technical School", "type": "TVET", "category": "Public", "province": province_name, "district": district_name},
        {"id": 2, "name": f"{district_name} Vocational School", "type": "TSS", "category": "Private", "province": province_name, "district": district_name}
    ]

@app.post("/api/v1/auth/register")
def register(data: dict):
    return {"message": "Registration successful"}

@app.post("/api/v1/auth/login")
def login(data: dict):
    return {"access_token": "token", "token_type": "bearer", "user": {"id": 1, "full_name": "Test", "email": data.get("email"), "role": "student"}}
