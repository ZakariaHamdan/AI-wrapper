# ai_service.py - Gemini AI integration
import os
import re
from google import genai
from google.genai import types
from typing import Dict, List, Optional, Any

from db_service import execute_sql_query
from file_service import load_context_files  # Updated import

# Load environment variables
API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBr2Zf6iJjgs-3mx54F61pRuWSUmLQcPB0")
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-001")

# Initialize the Gemini client
genai_client = genai.Client(api_key=API_KEY)

def get_system_instruction(context):
    """Create enhanced system instruction for the AI with model context"""
    return f"""
    You are a helpful AI assistant that specializes in database interactions using SQL Server.
    You're providing assistance through a web application that allows users to query the database.

    CRITICAL INSTRUCTION: When the user asks ANY question about data, users, records, or information that would be stored in a database, you MUST ALWAYS generate an SQL query to retrieve that information. DO NOT say that you cannot query the database - you CAN and SHOULD generate SQL queries for any data-related question.

    You have access to the following context files that define the application's data structure:
    {context}

    When asked about ANY data that might be in the database, ALWAYS:
    1. Generate an appropriate SQL query to answer the question
    2. Format the SQL query in a code block with ```sql tags
    3. The query will be executed automatically and results will be provided to you
    4. Then analyze the results and provide a clear, concise answer
    5. Keep in mind table names in the database should match the model class names

    RESPONSE FORMATTING INSTRUCTIONS:
    - Use HTML formatting in your responses for better readability in the web interface
    - Use <strong> or <b> tags for emphasis and important information
    - Use <ul> and <li> tags for lists
    - Use <p> tags for paragraphs
    - Include a concise summary at the beginning of your analysis
    - Use appropriate headings with <h4> tags for different sections
    - When presenting numerical results, consider using phrases like "There are X records" or "Found X matches"
    - Keep your responses concise and focused

    SQL query tips for SQL Server:
    - Use TOP clause for limiting results: SELECT TOP 10 * FROM Users
    - Use square brackets for table/column names with spaces: [User Name]
    - Use COUNT(*) for counting rows
    - JOIN syntax: SELECT u.Name FROM Users u JOIN Orders o ON u.UserId = o.UserId
    - For partial text matching use LIKE with wildcards: WHERE Name LIKE '%John%'
    - Use ORDER BY for sorting results: ORDER BY CreatedDate DESC
    - Consider performance by selecting only needed columns rather than using *
    - Use appropriate WHERE clauses to filter data effectively
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
            "You will be helping users query a SQL Server database. Remember to ALWAYS generate SQL queries for any data-related questions, use HTML formatting for readable responses, and provide concise analysis of results."
        )
    except Exception as e:
        print(f"Error priming chat session: {str(e)}")
    
    return chat

def process_message(chat, message, session_id, logger):
    """Process a chat message and determine if SQL query is needed"""
    from app import ChatResponse  # Import here to avoid circular imports

    # Check if this is a direct SQL query
    if message.strip().lower().startswith("select "):
        logger.info(f"Direct SQL query detected")
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
            logger.info(f"AI generated SQL query")
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
                    "<ul> and <li> for lists, and <h4> for section headings etc.. Start with a brief summary."
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
                logger.info(f"Data-related question detected")
                prompt_sql_response = chat.send_message(
                    f"The user's question appears to be about data in the database. Please generate an SQL query to answer this question: '{message}'. "
                    f"Format the query in a code block with ```sql tags. If you're absolutely certain this doesn't require database access, explain why."
                )
                
                # Check if the new response contains SQL
                sql_matches = sql_pattern.findall(prompt_sql_response.text)
                
                if sql_matches:
                    sql_query = sql_matches[0].strip()
                    logger.info(f"Generated SQL query on second attempt")
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