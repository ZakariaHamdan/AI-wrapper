# ai_service.py - Gemini AI integration for file analysis
import os
import sys
import logging
from typing import Dict, List, Optional, Any

# Add core to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.gemini_base import initialize_gemini, create_base_chat_session

# Set up logger
logger = logging.getLogger("gemini-file-analysis")

# Initialize Gemini client
gemini_client, model_name = initialize_gemini()

def get_file_analysis_system_instruction():
    """Create system instruction for file analysis"""
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

def create_chat_session():
    """Create a new chat session with Gemini for file analysis"""
    system_instruction = get_file_analysis_system_instruction()
    primer_message = "You will be helping users analyze and understand Excel and CSV files. Focus on extracting insights, explaining patterns, and providing clear explanations of the data."
    
    return create_base_chat_session(
        gemini_client, 
        model_name, 
        system_instruction, 
        primer_message
    )

def process_message(chat, message):
    """Process a chat message for file analysis"""
    try:
        # Send message to Gemini
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        return f"<p><b>Error:</b> There was a problem processing your request. Please try again.</p>"