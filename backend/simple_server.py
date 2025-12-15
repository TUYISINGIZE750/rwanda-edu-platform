#!/usr/bin/env python3
"""Simple FastAPI server with locations endpoints"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Rwanda Education Platform", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Server is running"}

@app.get("/")
def root():
    return {"message": "Rwanda Education Platform API"}

# Locations endpoints
@app.get("/api/v1/locations/provinces")
def get_provinces():
    return [
        {"name": "Kigali City"},
        {"name": "Southern Province"},
        {"name": "Western Province"},
        {"name": "Northern Province"},
        {"name": "Eastern Province"}
    ]

@app.get("/api/v1/locations/districts/{province_name}")
def get_districts(province_name: str):
    districts_map = {
        "Kigali City": ["Gasabo", "Kicukiro", "Nyarugenge"],
        "Southern Province": ["Kamonyi", "Muhanga", "Ruhango", "Nyanza", "Huye"],
        "Western Province": ["Karongi", "Rutsiro", "Rubavu", "Nyabihu"],
        "Northern Province": ["Rulindo", "Gakenke", "Musanze", "Burera"],
        "Eastern Province": ["Rwamagana", "Nyagatare", "Gatsibo", "Kayonza"]
    }
    districts = districts_map.get(province_name, [])
    return [{"name": district} for district in districts]

@app.get("/api/v1/locations/schools/district/{province_name}/{district_name}")
def get_schools(province_name: str, district_name: str):
    return [
        {
            "id": 1,
            "name": f"{district_name} Technical School",
            "type": "TVET",
            "category": "Public",
            "province": province_name,
            "district": district_name
        },
        {
            "id": 2,
            "name": f"{district_name} Vocational School",
            "type": "TSS",
            "category": "Private",
            "province": province_name,
            "district": district_name
        }
    ]

# Auth endpoints
@app.post("/api/v1/auth/register")
def register(user_data: dict):
    return {"message": "Registration successful", "user_id": 1}

@app.post("/api/v1/auth/login")
def login(credentials: dict):
    return {
        "access_token": "sample_token",
        "token_type": "bearer",
        "user": {
            "id": 1,
            "full_name": "Test User",
            "email": credentials.get("email"),
            "role": "student"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)