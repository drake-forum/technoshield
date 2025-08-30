#!/usr/bin/env python3

import os
import logging
import json
import yaml
from typing import Dict, Any

logger = logging.getLogger("technoshield-pipeline.utils.config")

# Default configuration
DEFAULT_CONFIG = {
    "processing_interval_seconds": 60,
    "data_sources": [
        {
            "name": "example_api",
            "type": "api",
            "url": "https://example.com/api/security-events",
            "headers": {"Content-Type": "application/json"},
            "auth": {
                "type": "bearer",
                "token": "YOUR_API_TOKEN"
            },
            "events_path": "data.events"
        }
    ],
    "alert_thresholds": {
        "authentication_failures": 3,
        "port_scan_threshold": 5
    },
    "logging": {
        "level": "INFO",
        "file": "pipeline.log"
    }
}


def load_config() -> Dict[str, Any]:
    """Load configuration from file or environment variables.
    
    Returns:
        Configuration dictionary
    """
    # Start with default configuration
    config = DEFAULT_CONFIG.copy()
    
    # Try to load configuration from file
    config_file = os.environ.get("PIPELINE_CONFIG_FILE", "config.yaml")
    config_from_file = load_config_from_file(config_file)
    if config_from_file:
        # Update default config with file config
        deep_update(config, config_from_file)
        logger.info(f"Loaded configuration from {config_file}")
    
    # Override with environment variables
    config = override_from_env(config)
    
    return config


def load_config_from_file(file_path: str) -> Dict[str, Any]:
    """Load configuration from a YAML or JSON file.
    
    Args:
        file_path: Path to the configuration file
        
    Returns:
        Configuration dictionary or None if file not found
    """
    if not os.path.exists(file_path):
        logger.warning(f"Configuration file not found: {file_path}")
        return None
    
    try:
        with open(file_path, 'r') as f:
            if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                return yaml.safe_load(f)
            elif file_path.endswith('.json'):
                return json.load(f)
            else:
                logger.warning(f"Unsupported configuration file format: {file_path}")
                return None
    except Exception as e:
        logger.error(f"Error loading configuration file: {str(e)}")
        return None


def override_from_env(config: Dict[str, Any]) -> Dict[str, Any]:
    """Override configuration values from environment variables.
    
    Args:
        config: Base configuration dictionary
        
    Returns:
        Updated configuration dictionary
    """
    # Processing interval
    if "PIPELINE_INTERVAL_SECONDS" in os.environ:
        try:
            config["processing_interval_seconds"] = int(os.environ["PIPELINE_INTERVAL_SECONDS"])
        except ValueError:
            pass
    
    # Logging level
    if "PIPELINE_LOG_LEVEL" in os.environ:
        config["logging"]["level"] = os.environ["PIPELINE_LOG_LEVEL"]
    
    # Alert thresholds
    if "PIPELINE_AUTH_FAILURES_THRESHOLD" in os.environ:
        try:
            config["alert_thresholds"]["authentication_failures"] = int(os.environ["PIPELINE_AUTH_FAILURES_THRESHOLD"])
        except ValueError:
            pass
    
    if "PIPELINE_PORT_SCAN_THRESHOLD" in os.environ:
        try:
            config["alert_thresholds"]["port_scan_threshold"] = int(os.environ["PIPELINE_PORT_SCAN_THRESHOLD"])
        except ValueError:
            pass
    
    return config


def deep_update(base_dict: Dict[str, Any], update_dict: Dict[str, Any]) -> None:
    """Recursively update a dictionary with another dictionary.
    
    Args:
        base_dict: Base dictionary to update
        update_dict: Dictionary with values to update
    """
    for key, value in update_dict.items():
        if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
            deep_update(base_dict[key], value)
        else:
            base_dict[key] = value