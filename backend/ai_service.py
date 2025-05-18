# ai_service.py - Gemini AI integration
import os
import re
from google import genai
from google.genai import types
from typing import Dict, List, Optional, Any

from db_service import execute_sql_query
from file_service import load_model_files

# Load environment variables
API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBr2Zf6iJjgs-3mx54F61pRuWSUmLQcPB0")
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-001")

# Initialize the Gemini client
genai_client = genai.Client(api_key=API_KEY)

def get_system_instruction(context):
    """Create enhanced system instruction for the AI with model context"""
    return f"""
    You are a helpful AI assistant that specializes in database interactions using various model files.
    You're running as a web API for a developer who needs quick database access.

    CRITICAL INSTRUCTION: When the user asks ANY question about data, users, records, or information that would be stored in a database, you MUST ALWAYS generate an SQL query to retrieve that information. DO NOT say that you cannot query the database - you CAN and SHOULD generate SQL queries for any data-related question.

    You have access to the following model files that define the application's data structure:
    {context}

    When asked about ANY data that might be in the database, ALWAYS:
    1. Generate an appropriate SQL query to answer the question
    2. Format the SQL query in a code block with ```sql tags
    3. The query will be executed automatically and results will be provided to you
    4. Then analyze the results and provide a clear, concise answer
    5. Keep in mind table names in the database should match the model class names

    The database is a SQL Server database, and you should use the model files to understand the table and column structure.

    SQL query tips for SQL Server:
    - Use TOP clause for limiting results: SELECT TOP 10 * FROM Users
    - Use square brackets for table/column names with spaces: [User Name]
    - Use COUNT(*) for counting rows
    - JOIN syntax: SELECT u.Name FROM Users u JOIN Orders o ON u.UserId = o.UserId
    - For partial text matching use LIKE with wildcards: WHERE Name LIKE '%John%'
    """

def create_chat_session(file_context):
    """Create a new chat session with Gemini"""
    chat = genai_client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=get_system_instruction(file_context),
            temperature=0.2
        )
    )
    
    # Prime the session
    try:
        chat.send_message(
            "You will be helping me query a SQL Server database. Remember to ALWAYS generate SQL queries for any data-related questions and use the model files to guide your queries."
        )
    except Exception as e:
        print(f"Error priming chat session: {str(e)}")
    
    return chat

def process_message(chat, message, session_id, logger):
    """Process a chat message and determine if SQL query is needed"""
    from app import ChatResponse  # Import here to avoid circular imports

    # Check if this is a direct SQL query
    if message.strip().lower().startswith("select "):
        logger.info(f"Processing direct SQL query from chat message")
        sql_query = message
        query_result, error = execute_sql_query(sql_query)
        
        if error:
            logger.warning(f"SQL Error in direct query: {error}")
            return ChatResponse(
                response=f"SQL Error: {error}",
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
                    "Please analyze these results and provide a concise interpretation."
                )
                interpretation = interpretation_response.text
            except Exception as e:
                logger.error(f"Error getting interpretation: {str(e)}")
                interpretation = f"Error getting interpretation: {str(e)}"
            
            return ChatResponse(
                response="Query executed successfully.",
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
            logger.info(f"SQL query detected in response: {sql_query[:50]}...")
            query_result, error = execute_sql_query(sql_query)
            
            if error:
                # Handle SQL execution errors
                logger.warning(f"SQL Error: {error}")
                interpretation_response = chat.send_message(
                    f"The SQL query failed with error: {error}\n\n"
                    "Please suggest an alternative query or explain what might be wrong."
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
                    "Please analyze these results and provide a concise, meaningful interpretation."
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
            if any(word in message.lower() for word in ["how many", "list", "show", "find", "get", "users", "count", "database", "data", "records"]):
                logger.info(f"Data-related question detected. Prompting for SQL query.")
                prompt_sql_response = chat.send_message(
                    f"Please generate an SQL query to answer this question: '{message}'. "
                    f"Format the query in a code block with ```sql tags."
                )
                
                # Check if the new response contains SQL
                sql_matches = sql_pattern.findall(prompt_sql_response.text)
                
                if sql_matches:
                    sql_query = sql_matches[0].strip()
                    logger.info(f"Generated SQL query: {sql_query[:50]}...")
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
                            "Please analyze these results and provide a concise, meaningful interpretation."
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
                    logger.info(f"No SQL query could be generated.")
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
        raise Exception(f"Error processing chat message: {str(e)}")