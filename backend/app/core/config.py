from pydantic import BaseModel, Field 
from functools import lru_cache 
from typing import Optional 
import os 
from dotenv import load_dotenv 
 
# Load environment variables 
load_dotenv() 
 
class Settings(BaseModel): 
    """Application settings using Pydantic BaseModel.""" 
    # API settings 
    API_HOST: str = Field(default=os.getenv("API_HOST", "0.0.0.0")) 
    API_PORT: int = Field(default=int(os.getenv("API_PORT", "8000"))) 
    BASE_URL: str = Field(default=os.getenv("BASE_URL", "http://localhost:8000")) 
 
    # Gemini API settings 
    GEMINI_API_KEY: str = Field(default=os.getenv("GEMINI_API_KEY", "")) 
    GEMINI_MODEL: str = Field(default=os.getenv("GEMINI_MODEL", "gemini-2.0-flash-001")) 
 
    # Database settings 
    DB_CONNECTION_STRING: Optional[str] = Field(default=os.getenv("DB_CONNECTION_STRING", None)) 
 
    # File settings 
    CONTEXT_FOLDER: str = Field(default=os.getenv("CONTEXT_FOLDER", "context")) 
    UPLOAD_FOLDER: str = Field(default=os.getenv("UPLOAD_FOLDER", "uploads")) 
 
    # Logging settings 
    LOG_LEVEL: str = Field(default=os.getenv("LOG_LEVEL", "INFO")) 
 
@lru_cache() 
def get_settings() -> Settings: 
    """Returns the application settings as a cached instance.""" 
    return Settings() 
