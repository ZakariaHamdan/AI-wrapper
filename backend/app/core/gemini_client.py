"""
Gemini AI client for interacting with Google's Gemini API.
IMPROVED VERSION - Simplified prompts for better performance
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
    
    def create_db_chat_session(self, context: str):
        """
        Create a chat session for database queries
        SQL SERVER SPECIFIC system instruction
        """
        system_instruction = f"""You are PHD, a helpful SQL SERVER database assistant. 

Database schema:
{context}

CRITICAL:When querying the EmployeeAttendance table always add the restriction to it that is ProjectId=64

IMPORTANT: Always generate Microsoft SQL Server compatible syntax:
- Use square brackets [TableName] for table/column names with spaces or reserved words
- Use TOP instead of LIMIT
- Use GETDATE() for current date/time
- Use LEN() instead of LENGTH()
- Use CHARINDEX() instead of LOCATE()
- Use ISNULL() for null handling
- When getting table names only use those table names :AggregatedCounter
                                                       Attedance1TO16MayBackup
                                                       AttendanceDevices
                                                       AttendanceExceptionBackup
                                                       AttendanceExceptionRequests
                                                       AttendanceExceptionTypes
                                                       AttendanceScheduleHolidays
                                                       AttendanceScheduleOverrides
                                                       AttendanceSchedules
                                                       ChangeReqBackup880040
                                                       ChangeRequestBackup
                                                       ChangeRequestTypes
                                                       Companies
                                                       CompanyPositionContracts
                                                       CompanyTypes
                                                       ContractorTypes
                                                       Counter
                                                       Countries
                                                       DailyAttendanceExceptions
                                                       DailyAttendanceResetHistory
                                                       EmployeeAttendance
                                                       EmployeeAttendanceLogs
                                                       EmployeeAttendanceLogsArchive
                                                       EmployeeAttendanceTemp
                                                       EmployeeCountries
                                                       EmployeePermanentExceptions
                                                       EmployeeProjects
                                                       EmployeePunchedProject
                                                       Employees
                                                       EmployeeScheduleOverrides
                                                       Hash
                                                       Import22Feb10
                                                       Import22Feb13
                                                       Import22Feb16
                                                       Import22Feb166
                                                       Import22Feb17
                                                       Import22Feb19
                                                       Import22Feb20
                                                       Import22Mar1
                                                       Import22Mar2
                                                       Import22Mars3
                                                       Import22Master
                                                       Job
                                                       JobParameter
                                                       JobPositions
                                                       JobQueue
                                                       JobSpecifications
                                                       LeaveRequestApprovals
                                                       LeaveRequests
                                                       LeaveTypes
                                                       List
                                                       MainContractors
                                                       PayrollPeriods
                                                       PositionCategories
                                                       Project
                                                       projectbackup
                                                       ProjectCompanies
                                                       ProjectDevices
                                                       PublicHolidays
                                                       Regions
                                                       Roles
                                                       Schema
                                                       Server
                                                       Set
                                                       State
                                                       sysdiagrams
                                                       TempApprovalRedirects
                                                       tempAtt20Nov
                                                       TransactionStatuses
                                                       UpdateEmployees2822
                                                       UserClaims
                                                       UserLogins
                                                       UserRoles
                                                       Users


Rules:
1. For data questions, generate SQL queries in ```sql``` blocks
2. Use HTML formatting: <b>, <ul>, <li>, <p> tags
3. Be concise and helpful
4. To get the table name for each table you can find them in BiovisionDbContext for example: public DbSet<Employee> Employees means entity Employee has table called Employees and public DbSet<EmployeeAttendance> EmployeeAttendance, entity EmployeeAttendance has table called EmployeeAttendance."""
        
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