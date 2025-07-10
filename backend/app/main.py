from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.api.endpoints import register_routes
from app.services.file_service import load_context_files
from app.services.db_service import set_connection_string

# Configure logging 
logger = configure_logging(logger_name="gemini-ai-service", log_file="api.log")

# Initialize settings 
settings = get_settings()

# Create FastAPI app 
app = FastAPI(
    title="Gemini AI Assistant API",
    description="AI-powered assistant using Gemini to help with database queries and file analysis",
    version="1.0.0"
)

# Add CORS middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log request information"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    path = request.url.path
    if not path.startswith("/static") and not path.endswith("favicon.ico"):
        logger.info(f"{request.method} {path} - Status: {response.status_code} - {process_time:.2f}s")
    return response

@app.on_event("startup")
async def startup_event():
    """Auto-discover database schema and initialize services on startup"""
    from app.services.schema_discovery import discover_database_schema

    # Initialize app state with default database (PA)
    app.state.current_database = "pa"  # Default database
    app.state.current_connection_string = settings.DB_CONNECTION_STRING

    # Set the connection string in db_service
    set_connection_string(settings.DB_CONNECTION_STRING)

    # Try to auto-discover schema first
    schema_context, error = discover_database_schema()

    if error:
        logger.warning(f"Schema auto-discovery failed: {error}")
        logger.info("Falling back to loading context files...")
        # Fallback to file-based context
        file_context, file_count, _ = load_context_files()
        app.state.db_context = file_context
        logger.info(f"Server started - Loaded {file_count} database context files (fallback)")
    else:
        app.state.db_context = schema_context
        logger.info(f"Server started - Auto-discovered schema for database: {app.state.current_database}")

# Register API routes 
register_routes(app)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "status": "Gemini AI Assistant API is running",
        "version": "1.0.0",
        "current_database": getattr(app.state, 'current_database', 'pa'),
        "endpoints": {
            "database": "/db/chat",
            "database_switch": "/db/switch-database",
            "current_database": "/db/current-database",
            "file_analysis": "/files/upload"
        }
    }

@app.get("/debug/config")
async def debug_config():
    """TEMPORARY: Debug configuration"""
    settings = get_settings()

    # Mask sensitive info
    debug_info = {
        "connection_string_exists": bool(settings.DB_CONNECTION_STRING),
        "connection_string_length": len(settings.DB_CONNECTION_STRING) if settings.DB_CONNECTION_STRING else 0,
        "connection_string_preview": settings.DB_CONNECTION_STRING[:50] + "..." if settings.DB_CONNECTION_STRING else None,
        "gemini_key_exists": bool(settings.GEMINI_API_KEY),
        "context_folder": settings.CONTEXT_FOLDER,
        "upload_folder": settings.UPLOAD_FOLDER,
        "current_database": getattr(app.state, 'current_database', 'unknown')
    }

    return debug_info

@app.get("/debug/schema")
async def debug_schema():
    """Debug endpoint to view discovered schema"""
    return {
        "current_database": getattr(app.state, 'current_database', 'unknown'),
        "schema_context": getattr(app.state, 'db_context', 'No schema loaded')
    }

@app.get("/debug/sessions")
async def debug_sessions():
    """Debug endpoint to view current sessions"""
    from app.services.ai_service import get_session_count
    return get_session_count()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)