# file_service.py - File loading and processing
import os
import glob
import re
import logging
from typing import Tuple, List, Dict, Set

logger = logging.getLogger("gemini-db-assistant")

# Define context files folder
CONTEXT_FILES_FOLDER = os.environ.get("CONTEXT_FILES_FOLDER", "./context_files")

def get_supported_file_types():
    """Returns a list of supported file types"""
    return [
        {"extension": ".cs", "description": "C# Model Files"},
        {"extension": ".py", "description": "Python Model Files"},
        {"extension": ".sql", "description": "SQL Schema Files"},
        {"extension": ".json", "description": "JSON Schema Files"},
        {"extension": ".ts", "description": "TypeScript Files"}
    ]

def detect_tables_from_cs(content: str) -> List[str]:
    """Extract table names from C# class definitions"""
    # Basic regex to find class declarations
    class_pattern = re.compile(r'class\s+(\w+)')
    tables = class_pattern.findall(content)
    return tables

def detect_tables_from_py(content: str) -> List[str]:
    """Extract table names from Python class definitions"""
    # Basic regex to find class declarations in Python
    class_pattern = re.compile(r'class\s+(\w+)')
    tables = class_pattern.findall(content)
    return tables

def detect_tables_from_sql(content: str) -> List[str]:
    """Extract table names from SQL create table statements"""
    # Basic regex to find CREATE TABLE statements
    table_pattern = re.compile(r'CREATE\s+TABLE\s+[\`\[\"]?(\w+)[\`\[\"]?', re.IGNORECASE)
    tables = table_pattern.findall(content)
    return tables

def detect_tables_from_json(content: str) -> List[str]:
    """Extract potential table names from JSON schema"""
    import json
    try:
        data = json.loads(content)
        # Look for objects that might represent tables
        if isinstance(data, dict):
            return list(data.keys())
        return []
    except:
        return []

def detect_tables_from_ts(content: str) -> List[str]:
    """Extract table names from TypeScript interface/class definitions"""
    # Basic regex to find interface/class declarations in TypeScript
    pattern = re.compile(r'(interface|class)\s+(\w+)')
    matches = pattern.findall(content)
    tables = [match[1] for match in matches]
    return tables

def process_file(file_path: str, content: str) -> Tuple[str, List[str]]:
    """Process a file based on its extension and extract tables"""
    ext = os.path.splitext(file_path)[1].lower()
    
    tables = []
    if ext == '.cs':
        tables = detect_tables_from_cs(content)
    elif ext == '.py':
        tables = detect_tables_from_py(content)
    elif ext == '.sql':
        tables = detect_tables_from_sql(content)
    elif ext == '.json':
        tables = detect_tables_from_json(content)
    elif ext == '.ts':
        tables = detect_tables_from_ts(content)
    
    # Format the content with file name for context
    formatted_content = f"\n\n--- {os.path.basename(file_path)} ---\n{content}"
    
    return formatted_content, tables

def load_model_files() -> Tuple[str, int, Set[str], List[str]]:
    """
    Load all supported model files from the context_files folder
    Returns:
    - combined context string
    - number of files loaded
    - set of detected tables
    - list of loaded file names
    """
    context = ""
    files_loaded = 0
    all_tables = set()
    file_names = []
    
    # Ensure the folder exists
    if not os.path.exists(CONTEXT_FILES_FOLDER):
        os.makedirs(CONTEXT_FILES_FOLDER)
        logger.info(f"Created context files directory: {CONTEXT_FILES_FOLDER}")
    
    # Get supported extensions
    supported_extensions = [file_type["extension"] for file_type in get_supported_file_types()]
    
    # Process each file
    for ext in supported_extensions:
        for file_path in glob.glob(os.path.join(CONTEXT_FILES_FOLDER, f"*{ext}")):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                    formatted_content, tables = process_file(file_path, content)
                    context += formatted_content
                    all_tables.update(tables)
                    
                    file_names.append(os.path.basename(file_path))
                    files_loaded += 1
                    
                    logger.info(f"Loaded file: {os.path.basename(file_path)}, detected tables: {tables}")
            except Exception as e:
                error_msg = f"Error reading {file_path}: {str(e)}"
                context += f"\n\n--- ERROR: {os.path.basename(file_path)} ---\n{error_msg}"
                logger.error(error_msg)
    
    # Get additional tables from database if available
    try:
        from db_service import get_table_schema
        db_tables = get_table_schema()
        all_tables.update(db_tables)
        
        logger.info(f"All detected tables: {sorted(list(all_tables))}")
    except Exception as e:
        logger.error(f"Error getting database schema: {str(e)}")
    
    return context, files_loaded, sorted(list(all_tables)), file_names