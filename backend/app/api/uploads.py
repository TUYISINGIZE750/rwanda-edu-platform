from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
from datetime import datetime
from ..core.database import get_db
from ..models.user import User
from ..core.security import get_current_user

router = APIRouter(prefix="/uploads", tags=["uploads"])

UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
    'video': ['.mp4', '.webm', '.mov', '.avi'],
    'audio': ['.mp3', '.wav', '.ogg', '.m4a'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.ppt', '.pptx', '.xls', '.xlsx']
}

os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_file_type(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    for file_type, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return file_type
    return 'document'

@router.post("/")
async def upload_files(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    uploaded_files = []
    
    for file in files:
        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        file_type = get_file_type(file.filename)
        file_size = len(content)
        
        uploaded_files.append({
            "filename": file.filename,
            "url": f"/uploads/{unique_filename}",
            "type": file_type,
            "size": file_size
        })
    
    return {"files": uploaded_files}

@router.get("/{filename}")
async def get_file(filename: str):
    from fastapi.responses import FileResponse
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path)
