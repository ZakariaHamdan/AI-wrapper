# app.py - Streamlined FastAPI application with routes
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional, Any
import logging
import time
import uuid
import os
import io
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import models
from models import ChatMessage, ChatResponse, ClearRequest, FileInfo

# Import our services
from ai_service import create_chat_session, process_message
from db_service import execute_sql_query
from file_service import load_context_files, get_supported_file_types, get_context_structure

# Configure logging - SIMPLIFIED
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("api.log")
    ]
)
logger = logging.getLogger("gemini-db-assistant")

# Get configuration from environment variables
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

def check_database_connection():
    """Test database connection and log the result"""
    try:
        # Try a simple query that should work with any SQL Server
        result, error = execute_sql_query("SELECT 1 AS ConnectionTest")
        
        if error:
            logger.error(f"⚠️ Database connection test failed with error: {error}")
            return False
        else:
            logger.info(f"✅ Database connection successful: {result}")
            return True
    except Exception as e:
        logger.error(f"⚠️ Database connection test failed with exception: {str(e)}")
        return False

        
# Create FastAPI app
app = FastAPI(title="SQL Database Assistant API", 
              description="AI-powered database assistant using Gemini to help users query and understand database schema and data")

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
file_context = None

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Simplified middleware to log only essential request information"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Only log non-static requests and skip favicon
    path = request.url.path
    if not path.startswith("/static") and not path.endswith("favicon.ico"):
        logger.info(f"{request.method} {path} - Status: {response.status_code} - {process_time:.2f}s")
    
    return response

@app.on_event("startup")
async def startup_event():
    """Load context files on startup and check database connection"""
    global file_context
    file_context, file_count, _ = load_context_files()
    logger.info(f"Server started - Loaded {file_count} context files")
    
    # Check database connection but don't prevent startup if it fails
    db_connected = check_database_connection()
    if not db_connected:
        logger.warning("Application started without database connection. SQL queries will fail.")
    else:
        logger.info("Application started with working database connection.")

@app.get("/")
async def root():
    """Root endpoint with minimal info"""
    file_info = load_context_files()
    return {
        "status": "SQL Database Assistant API is running", 
        "loaded_files": file_info[1],
        "supported_file_types": get_supported_file_types()
    }

@app.get("/config")
async def get_frontend_config():
    """Endpoint to provide frontend configuration"""
    return {
        "api_url": BASE_URL,
        "version": "1.0.0"
    }

@app.get("/context")
async def get_context():
    """Get information about loaded context files"""
    _, file_count, file_paths = load_context_files()
    return {
        "loaded_files": file_count,
        "folder": "context",
        "file_paths": file_paths
    }
    
@app.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatMessage):
    """Process a chat message and return the response"""
    request_id = str(uuid.uuid4())[:8]  # Use shorter ID for cleaner logs
    logger.info(f"Chat [{request_id}]: '{chat_request.message[:30]}...'")
    
    session_id = chat_request.session_id
    
    # Create a new session if none exists or if no session_id provided
    if not session_id or session_id not in chat_sessions:
        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = create_chat_session(file_context)
        logger.info(f"New chat session: {session_id[:8]}")
    
    # Get the chat session
    chat = chat_sessions[session_id]
    
    # Process the message
    response = process_message(chat, chat_request.message, session_id, logger)
    return response

@app.post("/clear")
async def clear_chat(clear_request: ClearRequest):
    """Clear a chat session"""
    session_id = clear_request.session_id
    
    if session_id in chat_sessions:
        # Create a new session with the same ID
        chat_sessions[session_id] = create_chat_session(file_context)
        logger.info(f"Cleared chat session: {session_id[:8]}")
        return {"status": "Chat session cleared", "session_id": session_id}
    else:
        logger.warning(f"Session not found: {session_id[:8]}")
        raise HTTPException(status_code=404, detail=f"Session not found")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), session_id: Optional[str] = None):
    """
    Upload an Excel or CSV file to be used in the conversation
    """
    request_id = str(uuid.uuid4())[:8]  # Use shorter ID for cleaner logs
    logger.info(f"File upload [{request_id}]: '{file.filename}'")
    
    # Validate file type
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ['.xlsx', '.xls', '.csv']:
        logger.warning(f"Invalid file type: {file_ext}")
        raise HTTPException(status_code=400, detail="Only .xlsx, .xls, and .csv files are supported")
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Import locally to avoid circular imports
        from file_processor import process_excel_file
        text_representation, file_stats = process_excel_file(file_content, file.filename)
        
        # Create a new session if none exists
        if not session_id or session_id not in chat_sessions:
            session_id = str(uuid.uuid4())
            chat_sessions[session_id] = create_chat_session(file_context)
            logger.info(f"New file upload session: {session_id[:8]}")
        
        # Get the chat session
        chat = chat_sessions[session_id]
        
        # Send file info to Gemini
        file_message = f"The user has uploaded a file: {file.filename}. Here is information about the file:\n\n{text_representation}"
        
        try:
            # Process the message
            response = chat.send_message(file_message)
            response_text = response.text
            
            return {
                "session_id": session_id,
                "response": response_text,
                "file_info": {
                    "filename": file.filename,
                    "rows": file_stats["rows"],
                    "columns": file_stats["columns"],
                    "column_names": file_stats["column_names"]
                }
            }
        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing file with AI: {str(e)}")
    
    except Exception as e:
        logger.error(f"Error processing file upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    # More concise logging for uvicorn
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "uvicorn": {"handlers": ["default"], "level": "INFO"},
            "uvicorn.error": {"level": "INFO"},
            "uvicorn.access": {"handlers": ["default"], "level": "INFO", "propagate": False},
        },
    }
    
    uvicorn.run("app:app", host=API_HOST, port=API_PORT, reload=True, log_config=log_config)