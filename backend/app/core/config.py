from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    
    # App
    PROJECT_NAME: str = "Rwanda Edu Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_BUCKET: str = "resources"
    
    # File limits
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".pdf", ".doc", ".docx", ".jpg", ".png", ".mp3", ".mp4"}
    
    # Moderation
    AUTO_APPROVE_TEACHERS: bool = True
    PROFANITY_CHECK_ENABLED: bool = True
    
    # Bandwidth
    LITE_MODE_THRESHOLD: int = 30 * 1024  # 30KB
    COMPRESSION_ENABLED: bool = True

settings = Settings()
