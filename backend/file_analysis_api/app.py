# app.py - File Analysis API
import os
import sys
import logging
import time
import uuid
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional, Any

# Add core to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.config import load_config
from core.file_processor import process_excel_file

# Load configuration
config = load_config()

# Import local services
from ai_service import create_chat_session, process_message
from models import ChatMessage, ChatResponse, ClearRequest, FileInfo

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("file_analysis_api.log")
    ]
)
logger = logging.getLogger("gemini-file-analysis")

# Get configuration
API_HOST = config.get("API_HOST", "0.0.0.0")
API_PORT = config.get("API_PORT", 8001)
BASE_URL = config.get("BASE_URL", "http://localhost:8001")

# Create FastAPI app
app = FastAPI(
    title="File Analysis Assistant API",
    description="AI-powered assistant using Gemini to help users analyze and understand Excel and CSV files"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store chat sessions
chat_sessions = {}

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log request information"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Only log non-static requests and skip favicon
    path = request.url.path
    if not path.startswith("/static") and not path.endswith("favicon.ico"):
        logger.info(f"{request.method} {path} - Status: {response.status_code} - {process_time:.2f}s")
    
    return response

@app.get("/")
async def root():
    """Root endpoint with minimal info"""
    return {
        "status": "File Analysis Assistant API is running",
        "version": "1.0.0"
    }

@app.get("/config")
async def get_frontend_config():
    """Endpoint to provide frontend configuration"""
    return {
        "api_url": BASE_URL,
        "version": "1.0.0"
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload an Excel or CSV file to be analyzed"""
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"File upload [{request_id}]: '{file.filename}'")
    
    # Validate file type
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ['.xlsx', '.xls', '.csv']:
        logger.warning(f"Invalid file type: {file_ext}")
        raise HTTPException(status_code=400, detail="Only .xlsx, .xls, and .csv files are supported")
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Process the file
        text_representation, file_stats = process_excel_file(file_content, file.filename)
        
        # Create a new session for file analysis
        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = create_chat_session()
        logger.info(f"New file analysis session: {session_id[:8]}")
        
        # Get the chat session
        chat = chat_sessions[session_id]
        
        # Send file info to Gemini with instructions
        file_message = (
            f"The user has uploaded a file: {file.filename}. "
            f"Here is information about the file:\n\n{text_representation}\n\n"
            f"Please analyze this data and be ready to answer questions about it. "
            f"Focus on helping the user understand patterns, insights, and statistics from this data."
        )
        
        # Process the message
        response = process_message(chat, file_message)
        
        return {
            "session_id": session_id,
            "response": response,
            "file_info": {
                "filename": file.filename,
                "rows": file_stats["rows"],
                "columns": file_stats["columns"],
                "column_names": file_stats["column_names"]
            }
        }
    except Exception as e:
        logger.error(f"Error processing file upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatMessage):
    """Process a chat message related to file analysis"""
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"Chat [{request_id}]: '{chat_request.message[:30]}...'")
    
    session_id = chat_request.session_id
    
    # Verify session exists
    if not session_id or session_id not in chat_sessions:
        logger.warning(f"Session not found: {session_id}")
        raise HTTPException(status_code=404, detail="Session not found. Please upload a file first.")
    
    # Get the chat session
    chat = chat_sessions[session_id]
    
    # Process the message
    response = process_message(chat, chat_request.message)
    
    return ChatResponse(
        response=response,
        session_id=session_id
    )

@app.post("/clear")
async def clear_chat(clear_request: ClearRequest):
    """Clear a chat session"""
    session_id = clear_request.session_id
    
    if session_id in chat_sessions:
        # Create a new session with the same ID
        chat_sessions[session_id] = create_chat_session()
        logger.info(f"Cleared chat session: {session_id[:8]}")
        return {"status": "Chat session cleared", "session_id": session_id}
    else:
        logger.warning(f"Session not found: {session_id[:8]}")
        raise HTTPException(status_code=404, detail=f"Session not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host=API_HOST, port=API_PORT, reload=True)