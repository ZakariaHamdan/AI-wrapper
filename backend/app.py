# app.py - Main FastAPI application with routes
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
from file_service import load_model_files, get_supported_file_types

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("api_debug.log")
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

# Create FastAPI app
app = FastAPI(title="Gemini Database Assistant API", 
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
    """Middleware to log request information"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"Request: {request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Process time: {process_time:.4f}s"
    )
    
    return response

@app.on_event("startup")
async def startup_event():
    """Load model files on startup"""
    global file_context
    file_context, file_count, tables, file_names = load_model_files()
    logger.info(f"API started. Loaded {file_count} files and discovered {len(tables)} database tables.")

@app.get("/")
async def root():
    """Root endpoint to check if API is running"""
    global file_context
    file_info = load_model_files()
    return {
        "status": "Gemini Database Assistant API is running", 
        "loaded_files": file_info[1],  # Access by index instead of unpacking
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
    """Get information about loaded schema files"""
    context, file_count, tables, file_names = load_model_files()
    return {
        "loaded_files": file_count,
        "tables": tables,
        "file_types": get_supported_file_types()
    }

@app.get("/context")
async def get_context():
    """Get information about loaded context files"""
    context, file_count, tables, file_names = load_model_files()
    return {
        "loaded_files": file_count,
        "folder": "model_files",
        "file_names": file_names
    }
    
@app.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatMessage):
    """Process a chat message and return the response"""
    request_id = str(uuid.uuid4())
    logger.info(f"Request {request_id}: Processing chat message: {chat_request.message[:30]}...")
    
    session_id = chat_request.session_id
    
    # Create a new session if none exists or if no session_id provided
    if not session_id or session_id not in chat_sessions:
        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = create_chat_session(file_context)
        logger.info(f"Created new chat session: {session_id}")
    
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
        logger.info(f"Cleared chat session: {session_id}")
        return {"status": "Chat session cleared", "session_id": session_id}
    else:
        logger.warning(f"Session ID not found: {session_id}")
        raise HTTPException(status_code=404, detail=f"Session ID {session_id} not found")

@app.post("/sql", response_model=ChatResponse)
async def direct_sql(sql_request: DirectSQLRequest):
    """Execute a direct SQL query"""
    session_id = sql_request.session_id
    
    # Create a new session if none exists or if no session_id provided
    if not session_id or session_id not in chat_sessions:
        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = create_chat_session(file_context)
        logger.info(f"Created new chat session for SQL query: {session_id}")
    
    # Get the chat session
    chat = chat_sessions[session_id]
    
    # Execute the SQL query
    logger.info(f"Executing direct SQL query: {sql_request.query[:50]}...")
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
            logger.info(f"SQL query executed successfully")
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
    uvicorn.run("app:app", host=API_HOST, port=API_PORT, reload=True)