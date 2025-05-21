"""
Logging configuration for the application.
Provides consistent logging setup across modules.
"""
import logging
import sys
from typing import Optional

from app.core.config import get_settings

def configure_logging(
    logger_name: str,
    log_file: Optional[str] = None,
    level: Optional[str] = None
) -> logging.Logger:
    """
    Configure and return a logger with consistent formatting
    
    Args:
        logger_name: Name of the logger to configure
        log_file: Optional file path to write logs to
        level: Optional log level override
        
    Returns:
        Configured logger instance
    """
    settings = get_settings()
    
    # Set log level from settings or parameter
    log_level_name = level or settings.LOG_LEVEL
    log_level = getattr(logging, log_level_name)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Get or create logger
    logger = logging.getLogger(logger_name)
    
    # Clear any existing handlers
    if logger.handlers:
        logger.handlers.clear()
    
    # Set logger level
    logger.setLevel(log_level)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if log file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_uvicorn_log_config(log_file: Optional[str] = None) -> dict:
    """
    Generate Uvicorn logging configuration dictionary
    
    Args:
        log_file: Optional file path for logging
        
    Returns:
        Dictionary with Uvicorn logging configuration
    """
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "uvicorn": {"handlers": ["default"], "level": "INFO"},
            "uvicorn.error": {"level": "INFO"},
            "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
        },
    }
    
    # Add file handlers if log file is specified
    if log_file:
        log_config["handlers"]["file"] = {
            "formatter": "default",
            "class": "logging.FileHandler",
            "filename": log_file,
        }
        log_config["handlers"]["access_file"] = {
            "formatter": "access",
            "class": "logging.FileHandler",
            "filename": log_file,
        }
        log_config["loggers"]["uvicorn"]["handlers"].append("file")
        log_config["loggers"]["uvicorn.access"]["handlers"].append("access_file")
    
    return log_config