import os
from google import genai
from google.genai import types
from typing import Dict, List, Optional, Any

def initialize_gemini(api_key=None, model_name=None):
    """Initialize and return a Gemini client"""
    api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
    model_name = model_name or os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-001")
    
    # Initialize the client
    client = genai.Client(api_key=api_key)
    
    return client, model_name

def create_base_chat_session(client, model_name, system_instruction, primer_message=None, temperature=0.2):
    """Create a new chat session with Gemini"""
    chat = client.chats.create(
        model=model_name,
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
            print(f"Error priming chat session: {str(e)}")
    
    return chat