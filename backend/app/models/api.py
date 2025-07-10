"""
API request and response models.
Uses Pydantic for validation.
UPDATED: Added structured table data support
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union

# Table data structure
class TableData(BaseModel):
    """Structured table data for SQL results"""
    headers: List[str]
    rows: List[List[Any]]
    row_count: int

# Common models
class SessionRequest(BaseModel):
    """Base class for chat session operations"""
    session_id: Optional[str] = None

class ChatMessage(SessionRequest):
    """Chat message request"""
    message: str

class ClearRequest(SessionRequest):
    """Clear chat session request"""
    pass

# Response models
class ChatResponse(BaseModel):
    """Base chat response model - UPDATED with structured table data"""
    response: str
    session_id: str
    has_sql: bool = False
    sql_query: Optional[str] = None
    sql_result: Optional[str] = None  # Keep for backward compatibility
    sql_table: Optional[TableData] = None  # NEW: Structured table data
    sql_error: Optional[str] = None
    user_question: Optional[str] = None
    interpretation: Optional[str] = None

class FileInfo(BaseModel):
    """Information about a file"""
    filename: str
    rows: int
    columns: int
    column_names: List[str]

class FileUploadResponse(BaseModel):
    """Response from file upload"""
    session_id: str
    response: str
    file_info: FileInfo

class ApiStatus(BaseModel):
    """API status information"""
    status: str
    version: str
    loaded_files: Optional[int] = None
    service_info: Optional[Dict[str, Any]] = None