"""
Centralized Logging Configuration
Implements structured logging with timestamp, severity, process name, and error handling.

Format: YYYY-MM-DD HH:MM:SS | LEVEL | PROCESS | Message
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class StructuredFormatter(logging.Formatter):
    """
    Custom formatter for structured logging.
    Format: YYYY-MM-DD HH:MM:SS | LEVEL | PROCESS | Message
    """
    
    def format(self, record):
        # Create timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Get process name from record or use default
        process_name = getattr(record, 'process_name', 'GENERAL')
        
        # Format the log message
        log_message = f"{timestamp} | {record.levelname} | {process_name} | {record.getMessage()}"
        
        return log_message


def setup_logger(
    name: str,
    log_file: Path,
    level: int = logging.INFO,
    process_name: Optional[str] = None
) -> logging.Logger:
    """
    Set up a structured logger with file and console handlers.
    
    Args:
        name: Logger name
        log_file: Path to log file
        level: Logging level (default: INFO)
        process_name: Process name for log identification
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers if they already exist
    if logger.handlers:
        return logger
    
    # Create log file directory if it doesn't exist
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Create formatter
    formatter = StructuredFormatter()
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Store process name in logger for use in formatter
    if process_name:
        logger.process_name = process_name
    
    return logger


def get_logger(name: str, process_name: Optional[str] = None) -> logging.Logger:
    """
    Get or create a logger with the specified name and process name.
    
    Args:
        name: Logger name
        process_name: Process name for log identification
        
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    
    # Set process name if provided
    if process_name:
        logger.process_name = process_name
    
    return logger


# Pre-configured loggers for different components
def get_pipeline_logger() -> logging.Logger:
    """Get logger for pipeline operations"""
    log_file = Path('logs/pipeline.log')
    return setup_logger('pipeline', log_file, process_name='PIPELINE')


def get_quality_logger() -> logging.Logger:
    """Get logger for data quality operations"""
    log_file = Path('logs/quality.log')
    return setup_logger('quality', log_file, process_name='QUALITY')


def get_analytics_logger() -> logging.Logger:
    """Get logger for analytics operations"""
    log_file = Path('logs/analytics.log')
    return setup_logger('analytics', log_file, process_name='ANALYTICS')


def get_airflow_logger() -> logging.Logger:
    """Get logger for Airflow operations"""
    log_file = Path('logs/airflow.log')
    return setup_logger('airflow', log_file, process_name='AIRFLOW')


def get_monitor_logger() -> logging.Logger:
    """Get logger for monitoring operations"""
    log_file = Path('logs/monitor.log')
    return setup_logger('monitor', log_file, process_name='MONITOR')


def log_error(logger: logging.Logger, message: str, exception: Optional[Exception] = None) -> None:
    """
    Log an error with optional exception details.
    
    Args:
        logger: Logger instance
        message: Error message
        exception: Optional exception object
    """
    if exception:
        logger.error(f"{message}: {str(exception)}", exc_info=True)
    else:
        logger.error(message)


def log_success(logger: logging.Logger, message: str) -> None:
    """
    Log a success message.
    
    Args:
        logger: Logger instance
        message: Success message
    """
    logger.info(f"✓ {message}")


def log_warning(logger: logging.Logger, message: str) -> None:
    """
    Log a warning message.
    
    Args:
        logger: Logger instance
        message: Warning message
    """
    logger.warning(f"⚠ {message}")
