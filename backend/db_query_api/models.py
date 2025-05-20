from pydantic import BaseModel
from typing import Dict, List, Optional, Any

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    has_sql: bool = False
    sql_query: Optional[str] = None
    sql_result: Optional[str] = None
    sql_error: Optional[str] = None
    interpretation: Optional[str] = None

class ClearRequest(BaseModel):
    session_id: str

class FileInfo(BaseModel):
    filename: str
    rows: int
    columns: int
    column_names: List[str]