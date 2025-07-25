"""
Database query API routes.
UPDATED: Now passes current database to AI service
"""
from fastapi import APIRouter, Depends, HTTPException, Request
import logging

from app.models.api import ChatMessage, ChatResponse, ClearRequest
from app.services.ai_service import process_db_message, clear_session
from app.services.db_service import check_database_connection
from app.core.logging import configure_logging

# Configure logging
logger = configure_logging(logger_name="db-query-routes")

# Create router
router = APIRouter()

@router.get("/status")
async def db_status():
    """Check database connection status"""
    db_connected = check_database_connection()

    if db_connected:
        return {"status": "connected"}
    else:
        return {"status": "disconnected"}

@router.post("/chat", response_model=ChatResponse)
async def db_chat(request: Request, chat_request: ChatMessage):
    """
    Process a database chat message and return the response
    UPDATED: Now passes current database to AI service
    
    Args:
        request: FastAPI request object
        chat_request: Chat message request
        
    Returns:
        ChatResponse with AI response and session info
    """
    request_id = chat_request.session_id or "new"
    logger.info(f"DB Chat [{request_id[:8]}]: '{chat_request.message[:30]}...'")

    # Access the context and current database from the app state
    context = request.app.state.db_context
    current_database = getattr(request.app.state, 'current_database', 'pa')  # Default to 'pa'

    logger.info(f"Processing request for database: {current_database}")

    # Process the message with database-specific instructions
    response = process_db_message(
        chat_request.message,
        chat_request.session_id,
        context,
        current_database  # ← NEW: Pass current database
    )

    return response

@router.post("/clear")
async def clear_db_chat(request: Request, clear_request: ClearRequest):
    """
    Clear a database chat session
    UPDATED: Now passes current database for proper session recreation
    
    Args:
        request: FastAPI request object
        clear_request: Clear request with session ID
        
    Returns:
        Status message
    """
    session_id = clear_request.session_id

    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID is required")

    # Get current database for proper session recreation
    current_database = getattr(request.app.state, 'current_database', 'pa')

    success = clear_session(session_id, current_database)  # ← NEW: Pass current database

    if success:
        logger.info(f"Cleared DB chat session: {session_id[:8]} for database: {current_database}")
        return {"status": "Chat session cleared", "session_id": session_id, "database": current_database}
    else:
        logger.warning(f"Session not found: {session_id[:8]}")
        raise HTTPException(status_code=404, detail=f"Session not found")