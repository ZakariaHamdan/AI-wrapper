"""
Database service for executing SQL queries.
UPDATED: Uses dynamic connection string from app state
"""
import pyodbc
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential
from typing import Tuple, Optional, Dict, List, Any

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.models.api import TableData

# Configure logging
logger = configure_logging(logger_name="db-service")

# Global variable to store current connection string
_current_connection_string = None

def set_connection_string(connection_string: str):
    """Set the current connection string for database operations"""
    global _current_connection_string
    _current_connection_string = connection_string
    logger.info("Updated database connection string")

def get_connection_string() -> str:
    """Get current connection string, fallback to settings if not set"""
    global _current_connection_string

    if _current_connection_string:
        return _current_connection_string

    # Fallback to settings
    settings = get_settings()
    return settings.DB_CONNECTION_STRING

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def execute_sql_query(query: str) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Execute SQL query against the database with retry logic
    UPDATED: Uses dynamic connection string
    
    Returns:
        Tuple of (result_data, error_message)
        result_data contains both 'text' and 'table' formats
    """
    # Get current connection string
    connection_string = get_connection_string()

    # DEBUG: Log connection string (masked for security)
    if connection_string:
        # Mask password for logging
        masked_conn = connection_string
        if "password=" in masked_conn.lower() or "pwd=" in masked_conn.lower():
            parts = masked_conn.split(';')
            masked_parts = []
            for part in parts:
                if 'password=' in part.lower() or 'pwd=' in part.lower():
                    masked_parts.append('PWD=***MASKED***')
                else:
                    masked_parts.append(part)
            masked_conn = ';'.join(masked_parts)
        logger.info(f"Connection string: {masked_conn}")
    else:
        logger.error("Connection string is None or empty!")
        return None, "Database connection string not configured. Please check your environment variables."

    try:
        # DEBUG: Log the original connection string processing
        logger.info(f"Original connection string length: {len(connection_string)}")

        # Fix any backslash issues in connection string
        original_conn = connection_string
        connection_string = connection_string.replace('\\\\', '\\')

        if original_conn != connection_string:
            logger.info("Applied backslash fix to connection string")

        logger.info("Attempting to connect to database...")

        # Connect to database
        conn = pyodbc.connect(connection_string)
        logger.info("Database connection successful!")

        cursor = conn.cursor()

        # Execute query
        logger.info(f"Executing query: {query}")
        cursor.execute(query)

        # Fetch results if it's a SELECT query
        if query.strip().upper().startswith("SELECT"):
            # Get column names
            column_names = [column[0] for column in cursor.description]

            # Fetch all rows
            rows = cursor.fetchall()

            # Convert to pandas DataFrame for text formatting (backward compatibility)
            df = pd.DataFrame.from_records(rows, columns=column_names)

            # Create text result (backward compatibility)
            text_result = df.to_string(index=False)
            text_result += f"\n\n({len(df)} rows returned)"

            # Create structured table data (NEW)
            table_data = TableData(
                headers=column_names,
                rows=[list(row) for row in rows],
                row_count=len(rows)
            )

            # Return both formats
            result = {
                "text": text_result,
                "table": table_data
            }
        else:
            # Non-SELECT query, return affected row count
            text_result = f"Query executed successfully. Rows affected: {cursor.rowcount}"
            result = {
                "text": text_result,
                "table": None
            }

        # Commit and close
        conn.commit()
        cursor.close()
        conn.close()

        logger.info(f"Query executed successfully, returning structured results")
        return result, None

    except Exception as e:
        error_message = str(e)
        logger.error(f"Database error details: {error_message}")
        logger.error(f"Error type: {type(e).__name__}")

        # DEBUG: Log more details about the error
        if hasattr(e, 'args'):
            logger.error(f"Error args: {e.args}")

        # Provide more specific error messages
        if "Login failed" in error_message:
            return None, f"Database authentication failed: {error_message}"
        elif "timeout" in error_message.lower():
            return None, "Database connection timed out. The server may be unavailable."
        elif "not found" in error_message.lower():
            return None, f"Database or server not found: {error_message}"
        elif "syntax error" in error_message.lower():
            return None, f"SQL syntax error in query: {error_message}"
        elif "permission" in error_message.lower():
            return None, "Insufficient permissions to execute the query."
        else:
            return None, f"Database error: {error_message}"

def check_database_connection():
    """
    Test database connection
    UPDATED: Works with dynamic connection string
    """
    try:
        logger.info("Testing database connection...")

        # Try a simple query
        result, error = execute_sql_query("SELECT 1 AS ConnectionTest")

        if error:
            logger.error(f"Database connection test failed with error: {error}")
            return False
        else:
            logger.info(f"Database connection test successful")
            return True
    except Exception as e:
        logger.error(f"Database connection test failed with exception: {str(e)}")
        return False

def execute_sql_query_with_connection(query: str, connection_string: str) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Execute SQL query with specific connection string (for testing connections)
    """
    # Temporarily store old connection string
    old_connection = get_connection_string()

    try:
        # Set new connection string
        set_connection_string(connection_string)

        # Execute query
        result, error = execute_sql_query(query)

        return result, error

    finally:
        # Restore old connection string
        set_connection_string(old_connection)