"""
API endpoints registration.
"""
from fastapi import FastAPI

from app.api.routes.db_query import router as db_router
from app.api.routes.file_analysis import router as file_router
from app.core.logging import configure_logging

def register_routes(app: FastAPI):
    """Register all API routes"""

    # Import route modules
    from app.api.routes.db_query import router as db_router
    from app.api.routes.file_analysis import router as file_router
    from app.api.routes.database_switch import router as db_switch_router

    # Register routes with prefixes
    app.include_router(db_router, prefix="/db", tags=["database"])
    app.include_router(file_router, prefix="/files", tags=["files"])
    app.include_router(db_switch_router, prefix="/db", tags=["database-switch"])