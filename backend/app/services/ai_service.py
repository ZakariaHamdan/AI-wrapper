"""
AI service for handling both database queries and file analysis.
FIXED: User question parameter properly passed
"""
import re
import uuid
from typing import Dict, Optional, Any

from app.core.gemini_client import GeminiClient
from app.core.logging import configure_logging
from app.models.api import ChatResponse
from app.services.db_service import execute_sql_query

# Configure logging
logger = configure_logging(logger_name="ai-service")

# Create a sessions cache
_chat_sessions = {}

# Initialize Gemini client
gemini_client = GeminiClient()

# Session management functions (unchanged)
def get_or_create_db_session(session_id: Optional[str], context: str) -> tuple:
    """Get existing or create new database chat session"""
    if not session_id or session_id not in _chat_sessions:
        session_id = str(uuid.uuid4())
        
        _chat_sessions[session_id] = {
            "type": "db_query",
            "chat": gemini_client.create_db_chat_session(context)
        }
        logger.info(f"Created new database chat session: {session_id[:8]}...")
    
    return session_id, _chat_sessions[session_id]["chat"]

def get_or_create_file_session(session_id: Optional[str]) -> tuple:
    """Get existing or create new file analysis chat session"""
    if not session_id or session_id not in _chat_sessions:
        session_id = str(uuid.uuid4())
        
        _chat_sessions[session_id] = {
            "type": "file_analysis",
            "chat": gemini_client.create_file_analysis_session()
        }
        logger.info(f"Created new file analysis session: {session_id[:8]}...")
    
    return session_id, _chat_sessions[session_id]["chat"]

def clear_session(session_id: str) -> bool:
    """Clear a chat session"""
    if session_id in _chat_sessions:
        session_type = _chat_sessions[session_id]["type"]
        
        if session_type == "db_query":
            # Reset with clean context
            _chat_sessions[session_id]["chat"] = gemini_client.create_db_chat_session("[Context has been reset]")
        else:
            _chat_sessions[session_id]["chat"] = gemini_client.create_file_analysis_session()
        
        logger.info(f"Cleared chat session: {session_id[:8]}...")
        return True
    
    logger.warning(f"Session not found for clearing: {session_id[:8]}...")
    return False

def process_db_message(message: str, session_id: Optional[str], context: str) -> ChatResponse:
    """
    Process a chat message for database queries
    FIXED: Properly passes user_question to helper functions
    """
    # Get or create session
    session_id, chat = get_or_create_db_session(session_id, context)
    
    # Handle direct SQL queries
    if message.strip().lower().startswith("select "):
        return _execute_direct_sql(message, session_id, chat, message)  # ← FIXED: Pass message as user_question
    
    # Regular chat message - let Gemini decide if SQL is needed
    try:
        response = chat.send_message(message)
        response_text = response.text
        
        # Check if Gemini generated SQL
        sql_matches = re.findall(r"```sql\s*(.*?)\s*```", response_text, re.DOTALL)
        
        if sql_matches:
            sql_query = sql_matches[0].strip()
            return _execute_generated_sql(sql_query, session_id, chat, message)  # ← FIXED: Pass message as user_question
        else:
            # No SQL needed - just return the response
            return ChatResponse(
                response=response_text,
                session_id=session_id,
                user_question=message
            )
                
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        return ChatResponse(
            response=f"<p><b>Error:</b> There was a problem processing your request. Please try again.</p>",
            session_id=session_id,
            user_question=message
        )

def _execute_direct_sql(sql_query: str, session_id: str, chat, user_question: str) -> ChatResponse:
    """Execute direct SQL query - FIXED: Added user_question parameter"""
    logger.info(f"Direct SQL query detected: {sql_query[:50]}...")
    query_result, error = execute_sql_query(sql_query)
    
    if error:
        return ChatResponse(
            response=f"<p><b>SQL Error:</b> {error}</p>",
            session_id=session_id,
            has_sql=True,
            sql_query=sql_query,
            sql_error=error,
            user_question=user_question  # ← FIXED: Now properly defined
        )
    else:
        # Use text result for AI interpretation
        text_result = query_result["text"]
        table_data = query_result["table"]
        
        # Simple interpretation request
        interpretation_response = chat.send_message(
            f"Analyze these SQL results and provide a concise summary:\n\n{text_result}\n\n"
            "Use HTML formatting with <b> tags for key points."
        )
        
        return ChatResponse(
            response=interpretation_response.text,
            session_id=session_id,
            has_sql=True,
            sql_query=sql_query,
            sql_result=text_result,  # Keep for backward compatibility
            sql_table=table_data,    # NEW: Structured table data
            user_question=user_question,  # ← FIXED: Now properly defined
            interpretation=interpretation_response.text
        )

def _execute_generated_sql(sql_query: str, session_id: str, chat, user_question: str) -> ChatResponse:
    """Execute SQL query generated by Gemini - FIXED: Added user_question parameter"""
    logger.info(f"AI generated SQL query: {sql_query[:50]}...")
    query_result, error = execute_sql_query(sql_query)
    
    if error:
        # Ask for alternative approach
        error_response = chat.send_message(
            f"The SQL query failed with: {error}\n\nSuggest an alternative approach."
        )
        
        return ChatResponse(
            response=error_response.text,
            session_id=session_id,
            has_sql=True,
            sql_query=sql_query,
            sql_error=error,
            user_question=user_question  # ← FIXED: Now properly defined
        )
    else:
        # Use text result for AI interpretation
        text_result = query_result["text"]
        table_data = query_result["table"]
        
        # Ask for analysis of results
        interpretation_response = chat.send_message(
            f"The SQL query returned:\n\n{text_result}\n\n"
            "Analyze these results and provide insights. Use HTML formatting."
        )
        
        return ChatResponse(
            response=interpretation_response.text,
            session_id=session_id,
            has_sql=True,
            sql_query=sql_query,
            sql_result=text_result,  # Keep for backward compatibility
            sql_table=table_data,    # NEW: Structured table data
            user_question=user_question,  # ← FIXED: Now properly defined
            interpretation=interpretation_response.text
        )

# Add this function anywhere in the file
def clear_all_sessions() -> int:
    """
    Clear all chat sessions (both db and file analysis)
    Returns number of sessions cleared
    """
    global _chat_sessions

    session_count = len(_chat_sessions)
    _chat_sessions.clear()

    logger.info(f"Cleared all chat sessions: {session_count} sessions removed")
    return session_count

def get_session_count() -> Dict[str, int]:
    """Get count of current sessions by type"""
    global _chat_sessions

    db_sessions = sum(1 for session in _chat_sessions.values() if session["type"] == "db_query")
    file_sessions = sum(1 for session in _chat_sessions.values() if session["type"] == "file_analysis")

    return {
        "total": len(_chat_sessions),
        "database": db_sessions,
        "file_analysis": file_sessions
    }

# File processing functions remain unchanged
def process_file_message(message: str, session_id: Optional[str]) -> ChatResponse:
    """Process a chat message for file analysis - UNCHANGED"""
    session_id, chat = get_or_create_file_session(session_id)
    
    try:
        response = chat.send_message(message)
        return ChatResponse(
            response=response.text,
            session_id=session_id
        )
    except Exception as e:
        logger.error(f"Error processing file analysis message: {str(e)}")
        return ChatResponse(
            response=f"<p><b>Error:</b> There was a problem processing your request. Please try again.</p>",
            session_id=session_id
        )

def process_file_upload(file_info: str, session_id: Optional[str]) -> ChatResponse:
    """Process uploaded file information - UNCHANGED"""
    session_id, chat = get_or_create_file_session(session_id)
    
    try:
        file_message = (
            f"The user has uploaded a file:\n\n{file_info}\n\n"
            f"Analyze this data and provide insights about patterns and statistics."
        )
        
        response = chat.send_message(file_message)
        
        return ChatResponse(
            response=response.text,
            session_id=session_id
        )
    except Exception as e:
        logger.error(f"Error processing file upload: {str(e)}")
        return ChatResponse(
            response=f"<p><b>Error:</b> There was a problem analyzing the file. Please try again.</p>",
            session_id=session_id
        )