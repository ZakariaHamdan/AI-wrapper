"""
File processing utilities.
Handles the processing of Excel and CSV files for analysis.
"""
import pandas as pd
import io
import os
from typing import Dict, List, Any, Tuple, Union
from fastapi import UploadFile

from app.core.logging import configure_logging

# Configure logging
logger = configure_logging(logger_name="file-processor")

async def process_file(file: UploadFile) -> Tuple[str, Dict[str, Any]]:
    """
    Process an uploaded file and convert it to a usable format for AI analysis
    
    Args:
        file: The uploaded file object
        
    Returns:
        Tuple of (text representation, metadata dictionary)
    """
    try:
        # Read file content
        file_content = await file.read()
        
        # Get file extension
        filename = file.filename
        extension = os.path.splitext(filename)[1].lower()
        
        # Create a BytesIO object
        file_obj = io.BytesIO(file_content)
        
        # Process based on file type
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
        
        # Enhanced stats for numeric data
        if df.select_dtypes(include=['number']).columns.any():
            file_stats["numeric_stats"] = df.describe().to_dict()
            
        # Missing value information
        file_stats["missing_values"] = df.isnull().sum().to_dict()
        
        # Convert to string representation for the conversation
        text_representation = (
            f"File: {filename}\n"
            f"Rows: {file_stats['rows']}, Columns: {file_stats['columns']}\n"
            f"Column names: {', '.join(file_stats['column_names'])}\n\n"
            f"Sample data:\n{df.head(10).to_string()}\n"
        )
        
        # Add summary statistics if available
        if "numeric_stats" in file_stats:
            text_representation += f"\nSummary statistics for numeric columns:\n{pd.DataFrame(file_stats['numeric_stats']).to_string()}\n\n"
        
        # Add missing values info
        missing_cols = {col: count for col, count in file_stats["missing_values"].items() if count > 0}
        if missing_cols:
            text_representation += "\nMissing values per column:\n"
            for col, count in missing_cols.items():
                text_representation += f"- {col}: {count} missing values\n"
        
        # Reset the file pointer for potential future reads
        await file.seek(0)
        
        return text_representation, file_stats
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise