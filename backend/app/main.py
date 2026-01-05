from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
import os
from .core.config import settings
from .core.redis_client import redis_client
from .core.timezone import rwanda_now_iso
from .api import auth, groups, messages, dm_requests, resources, incidents, sessions, websocket, admin, locations, registration, schools_by_district, modules, student_dashboard, teacher_dashboard, chat, direct_messages, simple_chat, uploads, reactions, replies, live_sessions, dos_admin, class_teacher, super_admin, inter_school, seed, cleanup, emergency, notifications

# Lazy import admin_schools to avoid pandas dependency issues
try:
    from .api import admin_schools
    HAS_ADMIN_SCHOOLS = True
except ImportError as e:
    print(f"Warning: admin_schools module not available: {e}")
    HAS_ADMIN_SCHOOLS = False

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# CORS - MUST be first, before any other middleware or mounts
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Compression for low bandwidth
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Create uploads directory if it doesn't exist
os.makedirs("uploads/resources", exist_ok=True)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(groups.router, prefix=settings.API_V1_STR)
app.include_router(messages.router, prefix=settings.API_V1_STR)
app.include_router(dm_requests.router, prefix=settings.API_V1_STR)
app.include_router(resources.router, prefix=settings.API_V1_STR)
app.include_router(incidents.router, prefix=settings.API_V1_STR)
app.include_router(sessions.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)
app.include_router(locations.router, prefix=settings.API_V1_STR)
app.include_router(registration.router, prefix=settings.API_V1_STR)
app.include_router(schools_by_district.router, prefix=settings.API_V1_STR)
app.include_router(modules.router, prefix=settings.API_V1_STR)
app.include_router(modules.teacher_router, prefix=settings.API_V1_STR)
app.include_router(student_dashboard.router, prefix=settings.API_V1_STR)
app.include_router(teacher_dashboard.router, prefix=settings.API_V1_STR)
app.include_router(chat.router, prefix=settings.API_V1_STR)
app.include_router(direct_messages.router, prefix=settings.API_V1_STR)
app.include_router(simple_chat.router, prefix=settings.API_V1_STR)
app.include_router(uploads.router, prefix=settings.API_V1_STR)
app.include_router(reactions.router, prefix=settings.API_V1_STR)
app.include_router(replies.router, prefix=settings.API_V1_STR)
app.include_router(live_sessions.router, prefix=settings.API_V1_STR)
app.include_router(dos_admin.router, prefix=settings.API_V1_STR)
app.include_router(class_teacher.router, prefix=settings.API_V1_STR)
app.include_router(super_admin.router, prefix=settings.API_V1_STR)
app.include_router(inter_school.router, prefix=settings.API_V1_STR)
app.include_router(seed.router, prefix=settings.API_V1_STR)
app.include_router(cleanup.router, prefix=settings.API_V1_STR)
app.include_router(emergency.router, prefix=settings.API_V1_STR)
app.include_router(notifications.router, prefix=settings.API_V1_STR)
if HAS_ADMIN_SCHOOLS:
    app.include_router(admin_schools.router, prefix=settings.API_V1_STR)
app.include_router(websocket.router)

@app.on_event("startup")
async def startup():
    await redis_client.connect()

@app.on_event("shutdown")
async def shutdown():
    await redis_client.disconnect()

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": settings.VERSION, "timestamp": rwanda_now_iso(), "timezone": "CAT (UTC+2)"}

@app.get("/api/v1/health")
def api_health_check():
    return {"status": "healthy", "api_version": "v1", "timestamp": rwanda_now_iso(), "timezone": "CAT (UTC+2)"}

@app.get("/api/v1/auth/test")
def auth_test():
    return {"status": "auth_service_healthy", "timestamp": rwanda_now_iso(), "timezone": "CAT (UTC+2)"}

@app.get("/wake-up")
def wake_up():
    """Dedicated wake-up endpoint with more processing to ensure full server activation"""
    import time
    start_time = time.time()
    
    # Simulate some processing to ensure server is fully awake
    dummy_data = [i**2 for i in range(1000)]
    processing_time = time.time() - start_time
    
    return {
        "status": "fully_awake",
        "message": "Server is active and processing requests",
        "processing_time_ms": round(processing_time * 1000, 2),
        "timestamp": rwanda_now_iso(),
        "timezone": "CAT (UTC+2) - Rwanda Time",
        "version": settings.VERSION
    }

@app.get("/api/v1/locations/schools/district/{province_name}/{district_name}")
def get_schools_hotfix(province_name: str, district_name: str):
    """Hotfix endpoint for schools dropdown"""
    from urllib.parse import unquote
    from .core.database import get_db
    from .models.school import School
    from sqlalchemy import func
    
    province_name = unquote(province_name)
    district_name = unquote(district_name)
    
    db = next(get_db())
    schools = db.query(School).filter(
        func.lower(School.province) == province_name.lower(),
        func.lower(School.district) == district_name.lower()
    ).all()
    
    return [{
        "id": s.id,
        "name": s.name,
        "type": s.type,
        "category": s.category,
        "province": s.province,
        "district": s.district,
        "trades": s.trades if hasattr(s, 'trades') else []
    } for s in schools]


