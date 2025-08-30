import logging
import logging.config
import os
from pathlib import Path
from typing import Dict, Any

# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Define logging configuration
LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {
            "()" : "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d %(funcName)s %(process)d %(thread)d %(exc_info)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "default",
            "filename": os.path.join("logs", "pipeline.log"),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8",
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "json",
            "filename": os.path.join("logs", "pipeline_error.log"),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8",
        },
        "data_collection_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "json",
            "filename": os.path.join("logs", "data_collection.log"),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8",
        },
        "threat_detection_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "json",
            "filename": os.path.join("logs", "threat_detection.log"),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "pipeline": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "pipeline.ingest": {
            "level": "INFO",
            "handlers": ["console", "data_collection_file"],
            "propagate": False,
        },
        "pipeline.analysis": {
            "level": "INFO",
            "handlers": ["console", "threat_detection_file"],
            "propagate": False,
        },
        "pipeline.errors": {
            "level": "ERROR",
            "handlers": ["console", "error_file"],
            "propagate": False,
        },
    },
    "root": {"level": "INFO", "handlers": ["console", "file"]},
}


def setup_logging() -> None:
    """Configure logging based on the defined configuration"""
    logging.config.dictConfig(LOGGING_CONFIG)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name"""
    return logging.getLogger(name)


# Data collection logging
def log_collection_event(source_type: str, details: Dict[str, Any]) -> None:
    """Log data collection events"""
    collection_logger = logging.getLogger("pipeline.ingest")
    log_data = {
        "source_type": source_type,
        "details": details,
    }
    
    collection_logger.info("Data collection event", extra=log_data)


# Threat detection logging
def log_threat_event(threat_type: str, severity: str, details: Dict[str, Any]) -> None:
    """Log threat detection events"""
    threat_logger = logging.getLogger("pipeline.analysis")
    log_data = {
        "threat_type": threat_type,
        "severity": severity,
        "details": details,
    }
    
    threat_logger.info("Threat detection event", extra=log_data)


# Error logging
def log_error(error_type: str, error_message: str, details: Dict[str, Any] = None) -> None:
    """Log pipeline errors"""
    error_logger = logging.getLogger("pipeline.errors")
    log_data = {
        "error_type": error_type,
        "error_message": error_message,
    }
    if details:
        log_data["details"] = details
    
    error_logger.error("Pipeline error", extra=log_data)