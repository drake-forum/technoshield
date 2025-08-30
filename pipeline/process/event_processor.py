#!/usr/bin/env python3

import logging
import json
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger("technoshield-pipeline.process")


def process_events(raw_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Process and normalize raw events from various sources.
    
    Args:
        raw_events: List of raw events collected from data sources
        
    Returns:
        List of processed and normalized events
    """
    processed_events = []
    
    for event in raw_events:
        try:
            # Determine the event type and use appropriate processor
            source_type = event.get('source_type', '').lower()
            
            if source_type == 'api':
                processed_event = process_api_event(event)
            elif source_type == 'file':
                processed_event = process_file_event(event)
            elif source_type == 'syslog':
                processed_event = process_syslog_event(event)
            else:
                # Default processing for unknown source types
                processed_event = process_generic_event(event)
            
            if processed_event:
                processed_events.append(processed_event)
                
        except Exception as e:
            logger.error(f"Error processing event: {str(e)}")
            logger.debug(f"Problematic event: {json.dumps(event, default=str)}")
    
    return processed_events


def process_api_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Process an event from an API source.
    
    Args:
        event: Raw event from an API source
        
    Returns:
        Processed and normalized event
    """
    # Create a new normalized event structure
    normalized = {
        'event_id': event.get('id') or generate_event_id(event),
        'timestamp': parse_timestamp(event),
        'source': {
            'name': event.get('source_name', 'unknown'),
            'type': 'api'
        },
        'event_type': determine_event_type(event),
        'severity': determine_severity(event),
        'description': extract_description(event),
        'raw_data': event,  # Store the original event for reference
        'processed_at': datetime.now().isoformat()
    }
    
    # Extract additional fields based on event structure
    if 'ip_address' in event:
        normalized['source_ip'] = event['ip_address']
    elif 'source_ip' in event:
        normalized['source_ip'] = event['source_ip']
    
    if 'user' in event:
        normalized['user'] = event['user']
    elif 'username' in event:
        normalized['user'] = event['username']
    
    return normalized


def process_file_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Process an event from a file source.
    
    Args:
        event: Raw event from a file source
        
    Returns:
        Processed and normalized event
    """
    # Similar to API event processing but with file-specific logic
    # This is a placeholder implementation
    return process_generic_event(event)


def process_syslog_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Process an event from a syslog source.
    
    Args:
        event: Raw event from a syslog source
        
    Returns:
        Processed and normalized event
    """
    # Similar to API event processing but with syslog-specific logic
    # This is a placeholder implementation
    return process_generic_event(event)


def process_generic_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Process an event with a generic approach when source-specific processing is not available.
    
    Args:
        event: Raw event from any source
        
    Returns:
        Processed and normalized event
    """
    # Create a new normalized event structure with basic fields
    normalized = {
        'event_id': event.get('id') or generate_event_id(event),
        'timestamp': parse_timestamp(event),
        'source': {
            'name': event.get('source_name', 'unknown'),
            'type': event.get('source_type', 'unknown')
        },
        'event_type': determine_event_type(event),
        'severity': determine_severity(event),
        'description': extract_description(event),
        'raw_data': event,  # Store the original event for reference
        'processed_at': datetime.now().isoformat()
    }
    
    return normalized


def generate_event_id(event: Dict[str, Any]) -> str:
    """Generate a unique ID for an event if it doesn't have one.
    
    Args:
        event: The event that needs an ID
        
    Returns:
        A unique event ID string
    """
    # Simple implementation - in production, use a more robust ID generation method
    import hashlib
    import time
    
    # Create a hash from the event data and current time
    event_str = json.dumps(event, sort_keys=True, default=str)
    hash_input = f"{event_str}-{time.time()}"
    return hashlib.md5(hash_input.encode()).hexdigest()


def parse_timestamp(event: Dict[str, Any]) -> str:
    """Extract and normalize the timestamp from an event.
    
    Args:
        event: The event containing a timestamp
        
    Returns:
        ISO-formatted timestamp string
    """
    # Look for common timestamp fields
    timestamp = None
    timestamp_fields = ['timestamp', 'time', 'date', 'created_at', 'event_time']
    
    for field in timestamp_fields:
        if field in event and event[field]:
            timestamp = event[field]
            break
    
    if not timestamp:
        # Use collection time if no timestamp is found
        timestamp = event.get('collection_time', datetime.now().isoformat())
    
    # Attempt to normalize the timestamp format if it's not already ISO format
    if isinstance(timestamp, str) and not timestamp.endswith('Z') and 'T' not in timestamp:
        try:
            # This is a very simplified approach - in production, use a more robust parser
            dt = datetime.fromisoformat(timestamp)
            return dt.isoformat()
        except (ValueError, TypeError):
            pass
    
    return str(timestamp)


def determine_event_type(event: Dict[str, Any]) -> str:
    """Determine the type of security event.
    
    Args:
        event: The event to categorize
        
    Returns:
        Event type string
    """
    # Look for explicit event type fields
    if 'event_type' in event:
        return event['event_type']
    if 'type' in event:
        return event['type']
    
    # Try to infer from content
    content = json.dumps(event, default=str).lower()
    
    if any(word in content for word in ['login', 'auth', 'password', 'credential']):
        return 'authentication'
    elif any(word in content for word in ['firewall', 'block', 'allow', 'network']):
        return 'network'
    elif any(word in content for word in ['malware', 'virus', 'trojan', 'ransomware']):
        return 'malware'
    elif any(word in content for word in ['permission', 'access', 'privilege']):
        return 'access_control'
    
    return 'unknown'


def determine_severity(event: Dict[str, Any]) -> str:
    """Determine the severity level of an event.
    
    Args:
        event: The event to evaluate
        
    Returns:
        Severity level string (critical, high, medium, low, info)
    """
    # Look for explicit severity fields
    for field in ['severity', 'priority', 'level', 'risk']:
        if field in event:
            severity = str(event[field]).lower()
            
            # Normalize different severity scales
            if severity in ['critical', 'high', 'medium', 'low', 'info']:
                return severity
            elif severity in ['1', '2', '3', '4', '5']:
                # Map numeric scale to text
                severity_map = {'1': 'critical', '2': 'high', '3': 'medium', '4': 'low', '5': 'info'}
                return severity_map.get(severity, 'medium')
            elif severity in ['emergency', 'alert', 'critical', 'error']:
                return 'critical'
            elif severity in ['warning']:
                return 'medium'
            elif severity in ['notice', 'info', 'debug']:
                return 'low'
    
    # Default severity if not found
    return 'medium'


def extract_description(event: Dict[str, Any]) -> str:
    """Extract a human-readable description from an event.
    
    Args:
        event: The event to describe
        
    Returns:
        Description string
    """
    # Look for common description fields
    for field in ['description', 'message', 'msg', 'detail', 'summary']:
        if field in event and event[field]:
            return str(event[field])
    
    # If no description field is found, create one from event type and source
    event_type = determine_event_type(event)
    source = event.get('source_name', 'unknown source')
    
    return f"{event_type.capitalize()} event from {source}"