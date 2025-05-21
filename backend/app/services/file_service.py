"""
File service for loading and managing context files.
"""
import os
from typing import Tuple, List, Dict, Any
import glob

from app.core.config import get_settings
from app.core.logging import configure_logging

# Configure logging
logger = configure_logging(logger_name="file-service")

# Get settings
settings = get_settings()

def get_supported_file_types() -> List[Dict[str, str]]:
    """Returns a list of supported file types"""
    return [
        {"extension": ".cs", "description": "C# Model Files"},
        {"extension": ".py", "description": "Python Model Files"},
        {"extension": ".sql", "description": "SQL Schema Files"},
        {"extension": ".json", "description": "JSON Schema Files"},
        {"extension": ".ts", "description": "TypeScript Files"}
    ]

def load_context_files() -> Tuple[str, int, List[str]]:
    """
    Load all supported files from the context folder and subfolders
    
    Returns:
        Tuple of (combined context string, number of files loaded, list of loaded file paths)
    """
    context = ""
    files_loaded = 0
    file_paths = []
    
    context_folder = settings.CONTEXT_FOLDER
    
    # Ensure the folder exists
    if not os.path.exists(context_folder):
        os.makedirs(context_folder)
        logger.info(f"Created context directory: {context_folder}")
        return context, files_loaded, file_paths
    
    # Get supported extensions
    supported_extensions = [file_type["extension"] for file_type in get_supported_file_types()]
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(context_folder):
        for file in files:
            # Check if file has supported extension
            if any(file.endswith(ext) for ext in supported_extensions):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, context_folder)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Format with file path for context
                        formatted_content = f"\n\n--- {rel_path} ---\n{content}"
                        context += formatted_content
                        
                        file_paths.append(rel_path)
                        files_loaded += 1
                        
                        logger.info(f"Loaded file: {rel_path}")
                except Exception as e:
                    error_msg = f"Error reading {rel_path}: {str(e)}"
                    context += f"\n\n--- ERROR: {rel_path} ---\n{error_msg}"
                    logger.error(error_msg)
    
    return context, files_loaded, file_paths

def ensure_upload_folder() -> str:
    """
    Ensures the upload folder exists and returns its path
    
    Returns:
        Path to the upload folder
    """
    upload_folder = settings.UPLOAD_FOLDER
    
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        logger.info(f"Created upload directory: {upload_folder}")
    
    return upload_folder

def get_context_structure() -> Dict[str, Any]:
    """
    Get a structured representation of the context folder
    
    Returns:
        Dictionary with folder structure and files
    """
    context_folder = settings.CONTEXT_FOLDER
    
    if not os.path.exists(context_folder):
        return {"folders": [], "files": []}
    
    supported_extensions = [file_type["extension"] for file_type in get_supported_file_types()]
    structure = {"folders": [], "files": []}
    
    for root, dirs, files in os.walk(context_folder):
        rel_root = os.path.relpath(root, context_folder)
        if rel_root == ".":
            # Files in the root context folder
            structure["files"] = [f for f in files if any(f.endswith(ext) for ext in supported_extensions)]
        else:
            # Create folder entry
            folder_entry = {
                "name": os.path.basename(root),
                "path": rel_root,
                "files": [f for f in files if any(f.endswith(ext) for ext in supported_extensions)]
            }
            structure["folders"].append(folder_entry)
    
    return structure