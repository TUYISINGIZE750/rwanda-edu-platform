@echo off
echo Quick Start - Simple Server
echo.

cd backend
echo Starting simple server on port 8000...
python -c "
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

@app.get('/health')
def health(): return {'status': 'ok'}

@app.get('/api/v1/locations/provinces')
def provinces(): return [{'name': 'Kigali City'}, {'name': 'Southern Province'}]

@app.get('/api/v1/locations/districts/{province}')
def districts(province: str): return [{'name': 'Kamonyi'}, {'name': 'Muhanga'}]

@app.get('/api/v1/locations/schools/district/{province}/{district}')
def schools(province: str, district: str): return [{'id': 1, 'name': f'{district} School', 'type': 'TVET', 'category': 'Public', 'province': province, 'district': district}]

uvicorn.run(app, host='0.0.0.0', port=8000)
"