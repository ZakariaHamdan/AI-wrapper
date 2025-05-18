# db_service.py - Focused database operations
import os
import pyodbc
import pandas as pd
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

# Get database connection string from environment variable
DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING", 
                                     "Driver={ODBC Driver 17 for SQL Server};Server=(localdb)\\mssqllocaldb;Database=Biovision;Trusted_Connection=yes;")

logger = logging.getLogger("gemini-db-assistant")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def execute_sql_query(query):
    """Execute SQL query against the database with retry logic and better error handling"""
    try:
        # Direct connection using pyodbc
        connection_string = DB_CONNECTION_STRING.replace('\\\\', '\\')
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute(query)
        
        # Fetch all rows
        if query.strip().upper().startswith("SELECT"):
            # Fetch column names
            column_names = [column[0] for column in cursor.description]
            
            # Fetch all rows
            rows = cursor.fetchall()
            
            # Convert to pandas DataFrame for better formatting
            df = pd.DataFrame.from_records(rows, columns=column_names)
            
            # Convert DataFrame to string representation
            result = df.to_string(index=False)
            
            # Add row count information
            row_count = len(df)
            result += f"\n\n({row_count} rows returned)"
        else:
            # For non-SELECT queries, just return affected rows
            result = f"Query executed successfully. Rows affected: {cursor.rowcount}"
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return result, None
    except Exception as e:
        error_message = str(e)
        logger.error(f"Database error: {error_message}")
        
        # More specific error messages for common issues
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