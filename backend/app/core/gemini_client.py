"""
Gemini AI client for interacting with Google's Gemini API.
IMPROVED VERSION - Simplified prompts for better performance
UPDATED: Added database-specific instructions
"""
from google import genai
from google.genai import types
from typing import Dict, List, Optional, Any

from app.core.config import get_settings
from app.core.logging import configure_logging

# Configure logging
logger = configure_logging(logger_name="gemini-client")

class GeminiClient:
    """
    Unified Gemini AI client for both database queries and file analysis.
    SIMPLIFIED for better performance and reliability.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        """Initialize Gemini client with API key and model"""
        settings = get_settings()
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model_name or settings.GEMINI_MODEL

        # Initialize the client
        try:
            self.client = genai.Client(api_key=self.api_key)
            logger.info(f"Initialized Gemini client with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {str(e)}")
            raise

    def create_chat_session(
            self,
            system_instruction: str,
            temperature: float = 0.1  # Lower temperature for more consistent responses
    ):
        """
        Create a new chat session with Gemini
        SIMPLIFIED - No primer messages to reduce API calls
        """
        try:
            chat = self.client.chats.create(
                model=self.model_name,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temperature
                )
            )

            return chat
        except Exception as e:
            logger.error(f"Error creating chat session: {str(e)}")
            raise

    def create_db_chat_session(self, context: str, database_name: str = "pa"):
        """
        Create a chat session for database queries
        SQL SERVER SPECIFIC system instruction with database-specific rules
        
        Args:
            context: Database schema context
            database_name: Current database name (pa, erp_mbl, erp_icad)
        """

        # Database-specific filtering rules
        if database_name.lower() in ['pa', 'erp_mbl']:
            attendance_filter_rule = "CRITICAL: When querying the EmployeeAttendance table always add the restriction ProjectId=64"
            logger.info(f"Applied ProjectId=64 filter for database: {database_name}")
        else:  # erp_icad or any other database
            attendance_filter_rule = "NOTE: No special ProjectId filtering required for EmployeeAttendance table in this database"
            logger.info(f"No ProjectId filter applied for database: {database_name}")

        system_instruction = f"""You are PHD, a helpful SQL SERVER database assistant. 

Current Database: {database_name.upper()}

Database schema:
{context}

{attendance_filter_rule}

IMPORTANT: Always generate Microsoft SQL Server compatible syntax:
- Use square brackets [TableName] for table/column names with spaces or reserved words
- Use TOP instead of LIMIT
- Use GETDATE() for current date/time
- Use LEN() instead of LENGTH()
- Use CHARINDEX() instead of LOCATE()
- Use ISNULL() for null handling

CRITICAL STRING MATCHING RULES:
- When users search for names or text values, ALWAYS use LIKE pattern matching with wildcards
- For example: "show me employee with name John" should use: WHERE EmployeeName LIKE '%John%'
- "find companies with name ABC" should use: WHERE CompanyName LIKE '%ABC%' 
- "employees in department HR" should use: WHERE Department LIKE '%HR%'
- Apply this pattern to ALL text searches including: names, descriptions, addresses, titles, departments, etc.
- Use '%searchterm%' to find partial matches, not exact equality (=)

ATTENDANCE & ABSENCE BUSINESS RULES:
- "Absent" does NOT mean no attendance record exists
- "Absent" means WorkHours = 0 or WorkHours IS NULL in the EmployeeAttendance table
- "Present" means WorkHours > 0
- When asked about "absent employees for last month", look for employees with attendance records WHERE (WorkHours IS NULL OR WorkHours <= 0)
- When asked about "present employees", look for employees WHERE WorkHours > 0
- Always consider WorkHours field as the primary indicator of attendance status

Rules:
1. For data questions, generate SQL queries in ```sql``` blocks
2. Use HTML formatting: <b>, <ul>, <li>, <p> tags
3. Be concise and helpful
4. Always use LIKE with wildcards for text searches unless user explicitly requests exact match"""

        return self.create_chat_session(system_instruction)

    def create_file_analysis_session(self):
        """
        Create a chat session for file analysis
        SIMPLIFIED system instruction
        """
        system_instruction = """You are a data analysis assistant.

Help users understand their Excel/CSV files by:
1. Explaining patterns and insights
2. Providing statistical summaries
3. Suggesting visualizations
4. Using HTML formatting: <b>, <ul>, <li>, <p> tags

Be concise and focus on actionable insights."""

        return self.create_chat_session(system_instruction)