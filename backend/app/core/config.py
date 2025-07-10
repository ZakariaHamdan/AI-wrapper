"""
Configuration management using environment variables.
UPDATED: Fixed Pydantic BaseSettings import
"""
import os
from pydantic_settings import BaseSettings  # ← Fixed import
import re

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    BASE_URL: str = "http://localhost:8000"

    # Gemini API Configuration
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-pro-experimental"

    # Database Configuration
    DB_CONNECTION_STRING: str

    # File Configuration
    CONTEXT_FOLDER: str = "context"
    UPLOAD_FOLDER: str = "uploads"

    # Logging Configuration
    LOG_LEVEL: str = "INFO"

    def get_connection_template(self) -> str:
        """Get connection string template for dynamic database switching"""
        if not self.DB_CONNECTION_STRING:
            return None

        # Extract template by removing specific database name
        # Assumes format: "...Database=DBNAME;..."
        template = re.sub(r'Database=[^;]+;', 'Database={database_name};', self.DB_CONNECTION_STRING)
        return template

    def build_connection_string(self, database_name: str) -> str:
        """Build connection string for specific database"""
        template = self.get_connection_template()
        if not template:
            return None
        return template.replace('{database_name}', database_name)

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create a global settings instance
_settings = None

def get_settings() -> Settings:
    """Get application settings (singleton pattern)"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings