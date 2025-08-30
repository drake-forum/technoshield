#!/usr/bin/env python3

import os
import json
import csv
import re
import requests
from typing import List, Dict, Any
from datetime import datetime

from pipeline.utils.logging_config import get_logger, log_collection_event, log_error
from pipeline.utils.metrics import record_data_collection, OperationTimer, start_metrics_server

logger = get_logger("pipeline.ingest")

# Start metrics server on port 8000
try:
    start_metrics_server(port=8000)
except Exception as e:
    logger.error(f"Failed to start metrics server: {str(e)}")


def collect_from_source(source_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Collect data from a single source based on its configuration.
    
    Args:
        source_config: Dictionary containing source configuration
        
    Returns:
        List of collected raw events
    """
    source_type = source_config.get('type', '').lower()
    source_name = source_config.get('name', 'unnamed')
    
    logger.info(f"Collecting data from {source_name} ({source_type})")
    
    # Use the OperationTimer context manager for timing and metrics
    with OperationTimer("data_collection", {"source": source_type}):
        try:
            if source_type == 'api':
                events = collect_from_api(source_config)
            elif source_type == 'file':
                events = collect_from_file(source_config)
            elif source_type == 'syslog':
                events = collect_from_syslog(source_config)
            else:
                logger.warning(f"Unknown source type: {source_type}")
                # Record metric for failed collection
                record_data_collection(source=source_type, status="error", data_points=0)
                return []
            
            # Record successful data collection metrics
            record_data_collection(source=source_type, status="success", data_points=len(events))
            
            # Log collection metrics
            log_collection_event(source_type, {
                "source_name": source_name,
                "events_count": len(events),
                "config": {k: v for k, v in source_config.items() if k not in ['auth', 'password', 'token', 'key']}
            })
            
            return events
        except Exception as e:
            # Record failed data collection metrics
            record_data_collection(source=source_type, status="error", data_points=0)
            
            log_error("collection_error", str(e), {
                "source_name": source_name,
                "source_type": source_type,
                "config": {k: v for k, v in source_config.items() if k not in ['auth', 'password', 'token', 'key']}
            })
            return []


def collect_from_all_sources(sources_config: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Collect data from all configured sources.
    
    Args:
        sources_config: List of source configurations
        
    Returns:
        Combined list of all collected raw events
    """
    all_events = []
    
    for source_config in sources_config:
        events = collect_from_source(source_config)
        if events:
            # Add source metadata to each event
            for event in events:
                event['source_name'] = source_config.get('name', 'unnamed')
                event['source_type'] = source_config.get('type', 'unknown')
                event['collection_time'] = datetime.now().isoformat()
            
            all_events.extend(events)
            logger.info(f"Collected {len(events)} events from {source_config.get('name', 'unnamed')}")
    
    return all_events


def collect_from_api(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Collect data from an API source.
    
    Args:
        config: API source configuration
        
    Returns:
        List of collected events
    """
    url = config.get('url')
    if not url:
        logger.error("API URL not provided in configuration")
        return []
    
    headers = config.get('headers', {})
    params = config.get('params', {})
    auth = None
    
    # Configure authentication if provided
    if 'auth' in config:
        auth_config = config['auth']
        auth_type = auth_config.get('type', '').lower()
        
        if auth_type == 'basic':
            auth = (auth_config.get('username', ''), auth_config.get('password', ''))
        elif auth_type == 'bearer':
            headers['Authorization'] = f"Bearer {auth_config.get('token', '')}" 
    
    try:
        response = requests.get(url, headers=headers, params=params, auth=auth, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        events = []
        
        # Extract events based on the path in the response
        events_path = config.get('events_path', '')
        if events_path:
            current_data = data
            for key in events_path.split('.'):
                if key in current_data:
                    current_data = current_data[key]
                else:
                    logger.warning(f"Could not find {key} in API response")
                    return []
            
            if isinstance(current_data, list):
                events = current_data
            else:
                logger.warning("Events path did not resolve to a list")
                return []
        else:
            # If no events_path is specified, assume the response is already a list of events
            if isinstance(data, list):
                events = data
            else:
                events = [data]  # Wrap single object in a list
        
        return events
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        return []
    except ValueError as e:
        logger.error(f"Failed to parse API response as JSON: {str(e)}")
        return []


def collect_from_file(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Collect data from a file source.
    
    Args:
        config: File source configuration
        
    Returns:
        List of collected events
    """
    file_path = config.get('path')
    if not file_path:
        logger.error("File path not provided in configuration")
        return []
    
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return []
    
    file_format = config.get('format', '').lower()
    events = []
    
    try:
        if file_format == 'json':
            events = collect_from_json_file(file_path, config)
        elif file_format == 'csv':
            events = collect_from_csv_file(file_path, config)
        elif file_format == 'log':
            events = collect_from_log_file(file_path, config)
        else:
            logger.warning(f"Unsupported file format: {file_format}")
            return []
            
        logger.info(f"Collected {len(events)} events from file {file_path}")
        return events
        
    except Exception as e:
        logger.error(f"Error collecting from file {file_path}: {str(e)}")
        return []


def collect_from_json_file(file_path: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Collect data from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        config: File source configuration
        
    Returns:
        List of collected events
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Extract events based on the path in the file
    events_path = config.get('events_path', '')
    if events_path:
        current_data = data
        for key in events_path.split('.'):
            if key in current_data:
                current_data = current_data[key]
            else:
                logger.warning(f"Could not find {key} in JSON file")
                return []
        
        if isinstance(current_data, list):
            return current_data
        else:
            logger.warning("Events path did not resolve to a list")
            return []
    else:
        # If no events_path is specified, assume the file contains a list of events
        if isinstance(data, list):
            return data
        else:
            return [data]  # Wrap single object in a list


def collect_from_csv_file(file_path: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Collect data from a CSV file.
    
    Args:
        file_path: Path to the CSV file
        config: File source configuration
        
    Returns:
        List of collected events
    """
    events = []
    
    with open(file_path, 'r', newline='') as f:
        # Use DictReader to automatically map columns to keys
        reader = csv.DictReader(f)
        for row in reader:
            # Convert empty strings to None
            event = {k: (v if v != '' else None) for k, v in row.items()}
            events.append(event)
    
    return events


def collect_from_log_file(file_path: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Collect data from a log file.
    
    Args:
        file_path: Path to the log file
        config: File source configuration
        
    Returns:
        List of collected events
    """
    events = []
    pattern = config.get('pattern', '')
    
    if not pattern:
        logger.warning("No regex pattern provided for log parsing")
        return []
    
    try:
        regex = re.compile(pattern)
        field_names = config.get('field_names', [])
        
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                    
                match = regex.search(line)
                if match:
                    if field_names:
                        # Use provided field names
                        event = {field_names[i]: group for i, group in enumerate(match.groups()) if i < len(field_names)}
                    else:
                        # Use group indices as field names
                        event = {f"field_{i}": group for i, group in enumerate(match.groups())}
                    
                    event['raw_message'] = line
                    events.append(event)
        
        return events
        
    except re.error as e:
        logger.error(f"Invalid regex pattern: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Error parsing log file: {str(e)}")
        return []


def collect_from_syslog(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Collect data from a syslog source.
    
    Args:
        config: Syslog source configuration
        
    Returns:
        List of collected events
    """
    syslog_path = config.get('path')
    if not syslog_path:
        logger.error("Syslog path not provided in configuration")
        return []
    
    if not os.path.exists(syslog_path):
        logger.error(f"Syslog file not found: {syslog_path}")
        return []
    
    # Syslog format: <priority>timestamp hostname process[pid]: message
    syslog_pattern = config.get('pattern', r'<(\d+)>([\w\s:]+)\s+([\w\.-]+)\s+([\w\.-]+)(?:\[(\d+)\])?:\s+(.+)')
    field_names = config.get('field_names', ['priority', 'timestamp', 'hostname', 'process', 'pid', 'message'])
    
    # Use the log file collector with syslog-specific pattern
    syslog_config = {
        'pattern': syslog_pattern,
        'field_names': field_names
    }
    
    events = collect_from_log_file(syslog_path, syslog_config)
    
    # Add syslog-specific processing if needed
    for event in events:
        if 'priority' in event:
            try:
                # Extract facility and severity from priority
                priority = int(event['priority'])
                event['facility'] = priority >> 3
                event['severity'] = priority & 0x7
            except (ValueError, TypeError):
                pass
    
    return events