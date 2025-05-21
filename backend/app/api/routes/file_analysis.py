"""
File analysis API routes.
"""
from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from typing import Optional
import uuid
import os

from app.models.api import ChatMessage, ChatResponse, ClearRequest, FileUploadResponse, FileInfo
from app.services.ai_service import process_file_message, process_file_upload, clear_session
from app.services.file_service import ensure_upload_folder
from app.utils.file_processor import process_file
from app.core.logging import configure_logging

# Configure logging
logger = configure_logging(logger_name="file-analysis-routes")

# Create router
router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    session_id: Optional[str] = Form(None)
):
    """
    Upload and analyze a file
    
    Args:
        file: Uploaded file
        session_id: Optional session ID
        
    Returns:
        FileUploadResponse with AI response and file info
    """
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"File upload [{request_id}]: '{file.filename}'")
    
    # Validate file type
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ['.xlsx', '.xls', '.csv']:
        logger.warning(f"Invalid file type: {file_ext}")
        raise HTTPException(
            status_code=400, 
            detail="Only .xlsx, .xls, and .csv files are supported"
        )
    
    try:
        # Process file
        text_representation, file_stats = await process_file(file)
        
        # Save file to upload folder
        upload_dir = ensure_upload_folder()
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as f:
            # Reset file cursor
            await file.seek(0)
            # Write file
            f.write(await file.read())
        
        # Get AI analysis
        response = process_file_upload(text_representation, session_id)
        
        # Create file info
        file_info = FileInfo(
            filename=file.filename,
            rows=file_stats["rows"],
            columns=file_stats["columns"],
            column_names=file_stats["column_names"]
        )
        
        # Return response
        return FileUploadResponse(
            session_id=response.session_id,
            response=response.response,
            file_info=file_info
        )
    
    except Exception as e:
        logger.error(f"Error processing file upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", response_model=ChatResponse)
async def file_chat(chat_request: ChatMessage):
    """
    Process a file analysis chat message
    
    Args:
        chat_request: Chat message request
        
    Returns:
        ChatResponse with AI response
    """
    session_id = chat_request.session_id
    
    if not session_id:
        raise HTTPException(
            status_code=400, 
            detail="Session ID is required. Please upload a file first."
        )
    
    logger.info(f"File chat [{session_id[:8]}]: '{chat_request.message[:30]}...'")
    
    # Process message
    response = process_file_message(chat_request.message, session_id)
    
    return response

@router.post("/clear")
async def clear_file_chat(clear_request: ClearRequest):
    """
    Clear a file analysis chat session
    
    Args:
        clear_request: Clear request with session ID
        
    Returns:
        Status message
    """
    session_id = clear_request.session_id
    
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID is required")
    
    success = clear_session(session_id)
    
    if success:
        logger.info(f"Cleared file chat session: {session_id[:8]}")
        return {"status": "Chat session cleared", "session_id": session_id}
    else:
        logger.warning(f"Session not found: {session_id[:8]}")
        raise HTTPException(status_code=404, detail=f"Session not found")