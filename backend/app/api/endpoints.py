"""
API endpoints registration.
"""
from fastapi import FastAPI

from app.api.routes.db_query import router as db_router
from app.api.routes.file_analysis import router as file_router
from app.core.logging import configure_logging

# Configure logging
logger = configure_logging(logger_name="api-endpoints")

def register_routes(app: FastAPI):
    """
    Register all API routes with the FastAPI app
    
    Args:
        app: FastAPI application instance
    """
    # Database query routes
    app.include_router(
        db_router,
        prefix="/db",
        tags=["Database Query"]
    )
    
    # File analysis routes
    app.include_router(
        file_router,
        prefix="/files",
        tags=["File Analysis"]
    )
    
    logger.info(f"API routes registered")