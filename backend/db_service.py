# db_service.py - Database operations
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
    """Execute SQL query against the database with retry logic"""
    try:
        # Direct connection using pyodbc
        conn = pyodbc.connect(DB_CONNECTION_STRING)
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
        logger.error(f"Database error: {str(e)}")
        return None, f"Database error: {str(e)}"

def get_table_schema():
    """Get schema information from the database"""
    try:
        conn = pyodbc.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        
        # Get all tables
        tables_query = """
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
        """
        
        cursor.execute(tables_query)
        tables = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return tables
    except Exception as e:
        logger.error(f"Error getting schema: {str(e)}")
        return []