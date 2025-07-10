"""
File processing utilities.
FIXED VERSION - Handle corrupted dates and large files
"""
import pandas as pd
import io
import os
from typing import Dict, List, Any, Tuple, Union
from fastapi import UploadFile
import warnings

from app.core.logging import configure_logging

# Configure logging
logger = configure_logging(logger_name="file-processor")

async def process_file(file: UploadFile) -> Tuple[str, Dict[str, Any]]:
    """
    Process an uploaded file and convert it to a usable format for AI analysis
    FIXED - Better error handling for corrupted data
    """
    try:
        # Read file content
        file_content = await file.read()
        
        # Check file size (add reasonable limit for demo)
        file_size_mb = len(file_content) / (1024 * 1024)
        logger.info(f"Processing file: {file.filename} ({file_size_mb:.1f} MB)")
        
        if file_size_mb > 50:  # 50MB limit for demo
            raise ValueError(f"File too large ({file_size_mb:.1f} MB). Please use files smaller than 50MB.")
        
        # Get file extension
        filename = file.filename
        extension = os.path.splitext(filename)[1].lower()
        
        # Create a BytesIO object
        file_obj = io.BytesIO(file_content)
        
        # Process based on file type with better error handling
        if extension in ['.xlsx', '.xls']:
            # Suppress openpyxl warnings about corrupted dates
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                # Read Excel file with error handling for dates
                df = pd.read_excel(file_obj, engine='openpyxl')
        elif extension == '.csv':
            # Read CSV file with encoding detection
            try:
                df = pd.read_csv(file_obj, encoding='utf-8')
            except UnicodeDecodeError:
                file_obj.seek(0)
                df = pd.read_csv(file_obj, encoding='latin-1')
        else:
            raise ValueError(f"Unsupported file type: {extension}")
        
        # Handle very large files - sample them for demo
        original_rows = len(df)
        if len(df) > 10000:
            logger.info(f"Large file detected ({original_rows} rows). Sampling first 10,000 rows for analysis.")
            df = df.head(10000)
        
        # Clean up any problematic columns for analysis
        df_clean = df.copy()
        for col in df_clean.columns:
            if df_clean[col].dtype == 'object':
                # Handle very long strings that might cause issues
                df_clean[col] = df_clean[col].astype(str).str[:1000]  # Truncate very long strings
        
        # Get basic stats about the file
        file_stats = {
            "rows": len(df_clean),
            "original_rows": original_rows,
            "columns": len(df_clean.columns),
            "column_names": list(df_clean.columns),
            "dtypes": {col: str(dtype) for col, dtype in df_clean.dtypes.items()},
            "sample_data": df_clean.head(5).to_dict(orient="records"),
            "file_size_mb": round(file_size_mb, 2)
        }
        
        # Enhanced stats for numeric data
        numeric_cols = df_clean.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            try:
                file_stats["numeric_stats"] = df_clean[numeric_cols].describe().to_dict()
            except Exception as e:
                logger.warning(f"Could not generate numeric stats: {e}")
                file_stats["numeric_stats"] = None
            
        # Missing value information
        file_stats["missing_values"] = df_clean.isnull().sum().to_dict()
        
        # Convert to string representation for the conversation
        if original_rows != len(df_clean):
            text_representation = (
                f"File: {filename} ({file_stats['file_size_mb']} MB)\n"
                f"Total Rows: {original_rows} (showing first {len(df_clean)} for analysis)\n"
                f"Columns: {file_stats['columns']}\n"
                f"Column names: {', '.join(file_stats['column_names'])}\n\n"
                f"Sample data (first 10 rows):\n{df_clean.head(10).to_string()}\n"
            )
        else:
            text_representation = (
                f"File: {filename} ({file_stats['file_size_mb']} MB)\n"
                f"Rows: {file_stats['rows']}, Columns: {file_stats['columns']}\n"
                f"Column names: {', '.join(file_stats['column_names'])}\n\n"
                f"Sample data (first 10 rows):\n{df_clean.head(10).to_string()}\n"
            )
        
        # Add summary statistics if available
        if file_stats.get("numeric_stats"):
            text_representation += f"\nSummary statistics for numeric columns:\n{pd.DataFrame(file_stats['numeric_stats']).to_string()}\n\n"
        
        # Add missing values info
        missing_cols = {col: count for col, count in file_stats["missing_values"].items() if count > 0}
        if missing_cols:
            text_representation += "\nMissing values per column:\n"
            for col, count in missing_cols.items():
                text_representation += f"- {col}: {count} missing values\n"
        
        # Reset the file pointer for potential future reads
        await file.seek(0)
        
        logger.info(f"Successfully processed file: {filename}")
        return text_representation, file_stats
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise