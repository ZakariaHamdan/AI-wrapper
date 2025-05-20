import os
from dotenv import load_dotenv

def load_config(env_path=None):
    """Load configuration from .env file"""
    if env_path:
        load_dotenv(env_path)
    else:
        load_dotenv()
    
    config = {
        # Gemini configuration
        "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY", ""),
        "GEMINI_MODEL": os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-001"),
        
        # API configuration
        "API_HOST": os.environ.get("API_HOST", "0.0.0.0"),
        "API_PORT": int(os.environ.get("API_PORT", "8000")),
        "BASE_URL": os.environ.get("BASE_URL", "http://localhost:8000"),
    }
    
    return config