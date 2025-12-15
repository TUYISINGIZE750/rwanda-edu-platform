from ..core.config import settings
import httpx
import uuid

async def upload_file(filename: str, content: bytes, content_type: str) -> str:
    """Upload file to Supabase Storage"""
    file_id = str(uuid.uuid4())
    file_path = f"{file_id}/{filename}"
    
    url = f"{settings.SUPABASE_URL}/storage/v1/object/{settings.SUPABASE_BUCKET}/{file_path}"
    
    headers = {
        "Authorization": f"Bearer {settings.SUPABASE_KEY}",
        "Content-Type": content_type
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, content=content, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Upload failed: {response.text}")
    
    return f"{settings.SUPABASE_URL}/storage/v1/object/public/{settings.SUPABASE_BUCKET}/{file_path}"
