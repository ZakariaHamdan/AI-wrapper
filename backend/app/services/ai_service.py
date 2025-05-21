"""
AI service for handling both database queries and file analysis.
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

# Session management
def get_or_create_db_session(session_id: Optional[str], context: str) -> tuple:
    """
    Get existing or create new database chat session
    
    Args:
        session_id: Optional session ID
        context: Database context information
        
    Returns:
        Tuple of (session_id, chat_session)
    """
    # Create new session ID if none provided or invalid
    if not session_id or session_id not in _chat_sessions:
        session_id = str(uuid.uuid4())
        
        # Create new session
        _chat_sessions[session_id] = {
            "type": "db_query",
            "chat": gemini_client.create_db_chat_session(context)
        }
        logger.info(f"Created new database chat session: {session_id[:8]}...")
    
    return session_id, _chat_sessions[session_id]["chat"]

def get_or_create_file_session(session_id: Optional[str]) -> tuple:
    """
    Get existing or create new file analysis chat session
    
    Args:
        session_id: Optional session ID
        
    Returns:
        Tuple of (session_id, chat_session)
    """
    # Create new session ID if none provided or invalid
    if not session_id or session_id not in _chat_sessions:
        session_id = str(uuid.uuid4())
        
        # Create new session
        _chat_sessions[session_id] = {
            "type": "file_analysis",
            "chat": gemini_client.create_file_analysis_session()
        }
        logger.info(f"Created new file analysis session: {session_id[:8]}...")
    
    return session_id, _chat_sessions[session_id]["chat"]

def clear_session(session_id: str) -> bool:
    """
    Clear a chat session
    
    Args:
        session_id: The session ID to clear
        
    Returns:
        Boolean indicating success
    """
    if session_id in _chat_sessions:
        session_type = _chat_sessions[session_id]["type"]
        
        if session_type == "db_query":
            _chat_sessions[session_id]["chat"] = gemini_client.create_db_chat_session(
                context="[Context has been reset]"
            )
        else:
            _chat_sessions[session_id]["chat"] = gemini_client.create_file_analysis_session()
        
        logger.info(f"Cleared chat session: {session_id[:8]}...")
        return True
    
    logger.warning(f"Session not found for clearing: {session_id[:8]}...")
    return False

# Process messages for database queries
def process_db_message(message: str, session_id: Optional[str], context: str) -> ChatResponse:
    """
    Process a chat message for database queries
    
    Args:
        message: The user message
        session_id: Optional session ID
        context: Database context information
        
    Returns:
        ChatResponse object
    """
    # Get or create session
    session_id, chat = get_or_create_db_session(session_id, context)
    
    # Check if this is a direct SQL query
    if message.strip().lower().startswith("select "):
        logger.info(f"Direct SQL query detected: {message[:50]}...")
        sql_query = message
        query_result, error = execute_sql_query(sql_query)
        
        if error:
            logger.warning(f"SQL Error: {error}")
            return ChatResponse(
                response=f"<p><b>SQL Error:</b> {error}</p>",
                session_id=session_id,
                has_sql=True,
                sql_query=sql_query,
                sql_error=error
            )
        else:
            # Ask Gemini to interpret the results
            try:
                interpretation_response = chat.send_message(
                    f"The SQL query '{sql_query}' returned the following results:\n\n{query_result}\n\n"
                    "Please analyze these results and provide a concise interpretation. "
                    "Use HTML formatting for better readability, including <b> tags for important information, "
                    "<ul> and <li> for lists, and <h4> for section headings. Start with a brief summary."
                )
                interpretation = interpretation_response.text
            except Exception as e:
                logger.error(f"Error getting interpretation: {str(e)}")
                interpretation = f"<p><b>Error:</b> Unable to interpret results: {str(e)}</p>"
            
            return ChatResponse(
                response=interpretation,
                session_id=session_id,
                has_sql=True,
                sql_query=sql_query,
                sql_result=query_result,
                interpretation=interpretation
            )
    
    # Regular chat message
    try:
        # Send message to Gemini
        response = chat.send_message(message)
        response_text = response.text
        
        # Look for SQL queries in the response
        sql_pattern = re.compile(r"```sql\s*(.*?)\s*```", re.DOTALL)
        sql_matches = sql_pattern.findall(response_text)
        
        # If an SQL query is found
        if sql_matches:
            sql_query = sql_matches[0].strip()
            logger.info(f"AI generated SQL query: {sql_query[:50]}...")
            query_result, error = execute_sql_query(sql_query)
            
            if error:
                # Handle SQL execution errors
                logger.warning(f"SQL Error: {error}")
                interpretation_response = chat.send_message(
                    f"The SQL query failed with error: {error}\n\n"
                    "Please suggest an alternative query or explain what might be wrong. "
                    "Format your response with HTML tags for better readability."
                )
                
                return ChatResponse(
                    response=interpretation_response.text,
                    session_id=session_id,
                    has_sql=True,
                    sql_query=sql_query,
                    sql_error=error
                )
            else:
                # Query executed successfully
                logger.info(f"SQL query executed successfully")
                interpretation_response = chat.send_message(
                    f"The SQL query returned the following results:\n\n{query_result}\n\n"
                    "Please analyze these results and provide a concise, meaningful interpretation. "
                    "Use HTML formatting for better readability, including <b> tags for important information, "
                    "<ul> and <li> for lists, and <h4> for section headings. Start with a brief summary."
                )
                
                return ChatResponse(
                    response=interpretation_response.text,
                    session_id=session_id,
                    has_sql=True,
                    sql_query=sql_query,
                    sql_result=query_result,
                    interpretation=interpretation_response.text
                )
        else:
            # If no SQL query was found but the question was data-related
            data_keywords = ["how many", "list", "show", "find", "get", "users", "count", 
                            "database", "data", "records", "total", "search", "query", 
                            "lookup", "fetch", "retrieve", "display"]
            
            if any(keyword in message.lower() for keyword in data_keywords):
                logger.info(f"Data-related question detected: {message[:50]}...")
                prompt_sql_response = chat.send_message(
                    f"The user's question appears to be about data in the database. Please generate an SQL query to answer this question: '{message}'. "
                    f"Format the query in a code block with ```sql tags. If you're absolutely certain this doesn't require database access, explain why."
                )
                
                # Check if the new response contains SQL
                sql_matches = sql_pattern.findall(prompt_sql_response.text)
                
                if sql_matches:
                    sql_query = sql_matches[0].strip()
                    logger.info(f"Generated SQL query on second attempt: {sql_query[:50]}...")
                    query_result, error = execute_sql_query(sql_query)
                    
                    if error:
                        logger.warning(f"SQL Error: {error}")
                        return ChatResponse(
                            response=prompt_sql_response.text,
                            session_id=session_id,
                            has_sql=True,
                            sql_query=sql_query,
                            sql_error=error
                        )
                    else:
                        logger.info(f"SQL query executed successfully")
                        interpretation_response = chat.send_message(
                            f"The SQL query returned the following results:\n\n{query_result}\n\n"
                            "Please analyze these results and provide a concise, meaningful interpretation. "
                            "Use HTML formatting for better readability, including <b> tags for important information, "
                            "<ul> and <li> for lists, and <h4> for section headings. Start with a brief summary."
                        )
                        
                        return ChatResponse(
                            response=interpretation_response.text,
                            session_id=session_id,
                            has_sql=True,
                            sql_query=sql_query,
                            sql_result=query_result,
                            interpretation=interpretation_response.text
                        )
                else:
                    # Still no SQL, just return the response
                    logger.info(f"No SQL query could be generated")
                    return ChatResponse(
                        response=prompt_sql_response.text,
                        session_id=session_id
                    )
            else:
                # Regular response (no SQL)
                logger.info(f"Regular response (no SQL needed)")
                return ChatResponse(
                    response=response_text,
                    session_id=session_id
                )
                
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        return ChatResponse(
            response=f"<p><b>Error:</b> There was a problem processing your request. Please try again.</p>",
            session_id=session_id
        )

# Process messages for file analysis
def process_file_message(message: str, session_id: Optional[str]) -> ChatResponse:
    """
    Process a chat message for file analysis
    
    Args:
        message: The user message
        session_id: Optional session ID
        
    Returns:
        ChatResponse object
    """
    # Get or create session
    session_id, chat = get_or_create_file_session(session_id)
    
    try:
        # Send message to Gemini
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

# Process file upload for analysis
def process_file_upload(file_info: str, session_id: Optional[str]) -> ChatResponse:
    """
    Process uploaded file information
    
    Args:
        file_info: Information about the uploaded file
        session_id: Optional session ID
        
    Returns:
        ChatResponse object
    """
    # Get or create session
    session_id, chat = get_or_create_file_session(session_id)
    
    try:
        # Send file info to Gemini
        file_message = (
            f"The user has uploaded a file. Here is information about the file:\n\n{file_info}\n\n"
            f"Please analyze this data and provide insights. "
            f"Focus on helping the user understand patterns, insights, and statistics from this data."
        )
        
        # Process the message
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