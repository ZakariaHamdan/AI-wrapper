"""
Gemini AI client for interacting with Google's Gemini API.
Centralizes AI functionality for both database and file analysis.
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
    Provides methods for creating chat sessions with different system instructions.
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
        primer_message: Optional[str] = None,
        temperature: float = 0.2
    ):
        """
        Create a new chat session with Gemini
        
        Args:
            system_instruction: The system instruction to initialize the model
            primer_message: Optional message to prime the session
            temperature: Temperature for generation (0.0 to 1.0)
            
        Returns:
            Chat session object
        """
        try:
            chat = self.client.chats.create(
                model=self.model_name,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temperature
                )
            )
            
            # Prime the session if provided
            if primer_message:
                try:
                    chat.send_message(primer_message)
                except Exception as e:
                    logger.warning(f"Error priming chat session: {str(e)}")
            
            return chat
        except Exception as e:
            logger.error(f"Error creating chat session: {str(e)}")
            raise
    
    def create_db_chat_session(self, context: str):
        """
        Create a chat session for database queries
        
        Args:
            context: Database schema information
            
        Returns:
            Configured chat session
        """
        system_instruction = self._get_db_system_instruction(context)
        primer_message = (
            "You will be helping users query a SQL Server database. "
            "Remember to ALWAYS generate SQL queries for any data-related questions, "
            "use HTML formatting for readable responses, and provide concise analysis of results."
        )
        
        return self.create_chat_session(system_instruction, primer_message)
    
    def create_file_analysis_session(self):
        """
        Create a chat session for file analysis
        
        Returns:
            Configured chat session
        """
        system_instruction = self._get_file_analysis_system_instruction()
        primer_message = (
            "You will be helping users analyze and understand Excel and CSV files. "
            "Focus on extracting insights, explaining patterns, and providing clear explanations of the data."
        )
        
        return self.create_chat_session(system_instruction, primer_message)
    
    def _get_db_system_instruction(self, context: str) -> str:
        """Create system instruction for the database query service"""
        return f"""
        You are a helpful AI assistant that specializes in database interactions using SQL Server.
        You're providing assistance through a web application that allows users to query the database.
        
        CRITICAL INSTRUCTION: When the user asks ANY question about data, users, records, or information 
        that would be stored in a database, you MUST ALWAYS generate an SQL query to retrieve that information. 
        DO NOT say that you cannot query the database - you CAN and SHOULD generate SQL queries for any data-related question.
        
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
        """
    
    def _get_file_analysis_system_instruction(self) -> str:
        """Create system instruction for file analysis service"""
        return """
        You are a helpful AI assistant that specializes in analyzing and explaining data from Excel and CSV files.
        
        Focus on:
        1. Understanding data patterns and trends
        2. Providing clear statistical insights
        3. Explaining relationships between variables
        4. Helping users understand their data through clear explanations
        5. Suggesting visualizations that would be appropriate for the data
        
        When analyzing data, always:
        1. Start with an overview of what you see in the data
        2. Point out any interesting patterns, outliers, or anomalies
        3. Suggest possible interpretations or conclusions
        4. Answer the user's specific questions about their data
        5. When appropriate, suggest further analyses that could provide more insights
        
        RESPONSE FORMATTING INSTRUCTIONS:
        - Use HTML formatting in your responses for better readability in the web interface
        - Use <strong> or <b> tags for emphasis and important information
        - Use <ul> and <li> tags for lists
        - Use <p> tags for paragraphs
        - Include a concise summary at the beginning of your analysis
        - Use appropriate headings with <h4> tags for different sections
        
        Remember: You are analyzing a file, NOT querying a database. Do not generate SQL code.
        """