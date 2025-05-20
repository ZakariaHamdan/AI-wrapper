# file_processor.py
import pandas as pd
import io
import os
import tempfile
import logging
from typing import Dict, List, Any, Tuple, Optional

logger = logging.getLogger("gemini-db-assistant")

def process_excel_file(file_content: bytes, filename: str) -> Tuple[str, Dict[str, Any]]:
    """
    Process an Excel file and convert it to a usable format for the AI conversation.
    
    Args:
        file_content: Raw bytes of the uploaded file
        filename: Original filename to determine the type
        
    Returns:
        Tuple of (text representation, metadata dictionary)
    """
    try:
        # Create a BytesIO object from the file content
        file_obj = io.BytesIO(file_content)
        
        # Determine file type from extension
        extension = os.path.splitext(filename)[1].lower()
        
        if extension in ['.xlsx', '.xls']:
            # Read Excel file
            df = pd.read_excel(file_obj, engine='openpyxl')
        elif extension == '.csv':
            # Read CSV file
            df = pd.read_csv(file_obj)
        else:
            raise ValueError(f"Unsupported file type: {extension}")
        
        # Get basic stats about the file
        file_stats = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "sample_data": df.head(5).to_dict(orient="records"),
        }
        
        # Convert to string representation for the conversation
        text_representation = (
            f"File: {filename}\n"
            f"Rows: {file_stats['rows']}, Columns: {file_stats['columns']}\n"
            f"Column names: {', '.join(file_stats['column_names'])}\n\n"
            f"Sample data:\n{df.head(10).to_string()}\n"
        )
        
        return text_representation, file_stats
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise