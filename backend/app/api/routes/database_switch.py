"""
Database switching API routes.
UPDATED: Properly handles session clearing with database context
"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import logging

from app.core.logging import configure_logging
from app.core.config import get_settings

# Configure logging
logger = configure_logging(logger_name="db-switch-routes")

# Create router
router = APIRouter()

class DatabaseSwitchRequest(BaseModel):
    database: str

class DatabaseSwitchResponse(BaseModel):
    status: str
    database: str
    message: str
    schema_preview: str = None

@router.post("/switch-database", response_model=DatabaseSwitchResponse)
async def switch_database(request: Request, switch_request: DatabaseSwitchRequest):
    """
    Switch to a different database and clear all sessions
    UPDATED: Passes database context when clearing sessions
    
    Args:
        request: FastAPI request object
        switch_request: Database switch request
        
    Returns:
        DatabaseSwitchResponse with switch result
    """
    database_name = switch_request.database.strip().lower()
    logger.info(f"Database switch requested: {database_name}")

    try:
        # Import here to avoid circular imports
        from app.services.schema_discovery import discover_database_schema_with_connection
        from app.services.ai_service import clear_all_sessions
        from app.services.db_service import set_connection_string

        # Build new connection string
        settings = get_settings()
        new_connection_string = settings.build_connection_string(database_name)

        if not new_connection_string:
            raise HTTPException(status_code=400, detail="Could not build connection string")

        logger.info(f"Built connection string for database: {database_name}")

        # Discover schema with new connection first (to validate connection)
        schema_context, error = discover_database_schema_with_connection(new_connection_string)

        if error:
            logger.error(f"Schema discovery failed for {database_name}: {error}")
            return DatabaseSwitchResponse(
                status="error",
                database=database_name,
                message=f"Failed to connect to database '{database_name}': {error}"
            )

        # Update app state FIRST (before clearing sessions)
        request.app.state.db_context = schema_context
        request.app.state.current_database = database_name
        request.app.state.current_connection_string = new_connection_string

        # Update the global connection string in db_service
        set_connection_string(new_connection_string)

        # Clear all existing chat sessions AFTER updating app state
        # This ensures any new sessions created will use the new database context
        cleared_count = clear_all_sessions()
        logger.info(f"Cleared {cleared_count} chat sessions for database switch to: {database_name}")

        # Create preview of schema (first 500 chars)
        schema_preview = schema_context[:500] + "..." if len(schema_context) > 500 else schema_context

        # Log database-specific rules
        if database_name.lower() in ['pa', 'erp_mbl']:
            logger.info(f"Database {database_name}: ProjectId=64 filter will be applied to EmployeeAttendance queries")
        else:
            logger.info(f"Database {database_name}: No ProjectId filter will be applied to EmployeeAttendance queries")

        logger.info(f"Successfully switched to database: {database_name}")

        return DatabaseSwitchResponse(
            status="success",
            database=database_name,
            message=f"Successfully switched to database '{database_name}'. All sessions cleared and database-specific rules applied.",
            schema_preview=schema_preview
        )

    except Exception as e:
        error_msg = f"Error switching database: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/current-database")
async def get_current_database(request: Request):
    """Get currently selected database with rule information"""
    current_db = getattr(request.app.state, 'current_database', 'pa')  # Default to 'pa'

    # Add database-specific rule information
    if current_db.lower() in ['pa', 'erp_mbl']:
        filter_info = "ProjectId=64 filter applied to EmployeeAttendance"
    else:
        filter_info = "No ProjectId filter applied"

    return {
        "current_database": current_db,
        "filter_rules": filter_info,
        "like_matching": "Enabled for all text searches"
    }