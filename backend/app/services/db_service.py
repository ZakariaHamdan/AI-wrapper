"""
Database service for executing SQL queries.
"""
import pyodbc
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import get_settings
from app.core.logging import configure_logging

# Configure logging
logger = configure_logging(logger_name="db-service")

# Get settings
settings = get_settings()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def execute_sql_query(query: str):
    """
    Execute SQL query against the database with retry logic
    
    Args:
        query: SQL query to execute
        
    Returns:
        Tuple of (result, error)
    """
    # Get connection string from settings
    connection_string = settings.DB_CONNECTION_STRING
    
    if not connection_string:
        logger.error("Database connection string not configured")
        return None, "Database connection string not configured. Please check your environment variables."
    
    try:
        # Fix any backslash issues in connection string
        connection_string = connection_string.replace('\\\\', '\\')
        
        # Connect to database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # Execute query
        cursor.execute(query)
        
        # Fetch results if it's a SELECT query
        if query.strip().upper().startswith("SELECT"):
            # Get column names
            column_names = [column[0] for column in cursor.description]
            
            # Fetch all rows
            rows = cursor.fetchall()
            
            # Convert to pandas DataFrame for formatting
            df = pd.DataFrame.from_records(rows, columns=column_names)
            
            # Convert DataFrame to string
            result = df.to_string(index=False)
            
            # Add row count information
            row_count = len(df)
            result += f"\n\n({row_count} rows returned)"
        else:
            # Non-SELECT query, return affected row count
            result = f"Query executed successfully. Rows affected: {cursor.rowcount}"
        
        # Commit and close
        conn.commit()
        cursor.close()
        conn.close()
        
        return result, None
    except Exception as e:
        error_message = str(e)
        logger.error(f"Database error: {error_message}")
        
        # Provide more specific error messages
        if "Login failed" in error_message:
            return None, "Database authentication failed. Please check credentials."
        elif "timeout" in error_message.lower():
            return None, "Database connection timed out. The server may be unavailable."
        elif "not found" in error_message.lower():
            return None, "Database or server not found. Please check configuration."
        elif "syntax error" in error_message.lower():
            return None, f"SQL syntax error in query: {error_message}"
        elif "permission" in error_message.lower():
            return None, "Insufficient permissions to execute the query."
        else:
            return None, f"Database error: {error_message}"

def check_database_connection():
    """
    Test database connection
    
    Returns:
        Boolean indicating connection success
    """
    try:
        # Try a simple query
        result, error = execute_sql_query("SELECT 1 AS ConnectionTest")
        
        if error:
            logger.error(f"Database connection test failed with error: {error}")
            return False
        else:
            logger.info(f"Database connection successful: {result}")
            return True
    except Exception as e:
        logger.error(f"Database connection test failed with exception: {str(e)}")
        return False