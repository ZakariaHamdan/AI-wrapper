# app.py - Streamlined FastAPI application with routes
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import logging
import time
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

# Models for request/response
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    has_sql: bool = False
    sql_query: Optional[str] = None
    sql_result: Optional[str] = None
    sql_error: Optional[str] = None
    interpretation: Optional[str] = None

class ClearRequest(BaseModel):
    session_id: str

class DirectSQLRequest(BaseModel):
    query: str
    session_id: Optional[str] = None


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

@app.get("/schema")
async def get_schema():
    """Get information about loaded context files only - no database schema"""
    context_structure = get_context_structure()
    
    # Create empty tables array for frontend compatibility
    empty_tables = []
    
    return {
        "tables": empty_tables,
        "file_types": get_supported_file_types(),
        "context_structure": context_structure
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

@app.post("/sql", response_model=ChatResponse)
async def direct_sql(sql_request: DirectSQLRequest):
    """Execute a direct SQL query"""
    session_id = sql_request.session_id
    
    # Create a new session if none exists or if no session_id provided
    if not session_id or session_id not in chat_sessions:
        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = create_chat_session(file_context)
        logger.info(f"New SQL session: {session_id[:8]}")
    
    # Get the chat session
    chat = chat_sessions[session_id]
    
    # Execute the SQL query
    logger.info(f"SQL: '{sql_request.query[:50]}...'")
    query_result, error = execute_sql_query(sql_request.query)
    
    if error:
        logger.warning(f"SQL Error: {error}")
        return ChatResponse(
            response=f"SQL Error: {error}",
            session_id=session_id,
            has_sql=True,
            sql_query=sql_request.query,
            sql_error=error
        )
    else:
        # Ask AI to interpret the results
        try:
            logger.info(f"SQL executed successfully")
            interpretation_prompt = f"The SQL query '{sql_request.query}' returned the following results:\n\n{query_result}\n\nPlease analyze these results and provide a concise interpretation."
            interpretation_response = chat.send_message(interpretation_prompt)
            interpretation = interpretation_response.text
        except Exception as e:
            logger.error(f"Error getting interpretation: {str(e)}")
            interpretation = f"Error getting interpretation: {str(e)}"
        
        return ChatResponse(
            response="Query executed successfully.",
            session_id=session_id,
            has_sql=True,
            sql_query=sql_request.query,
            sql_result=query_result,
            interpretation=interpretation
        )

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