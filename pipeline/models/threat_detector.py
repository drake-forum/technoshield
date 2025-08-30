#!/usr/bin/env python3

from typing import List, Dict, Any
from datetime import datetime

from pipeline.utils.logging_config import get_logger, log_threat_event, log_error
from pipeline.utils.metrics import record_threat_detection, OperationTimer, start_metrics_server

logger = get_logger("pipeline.analysis")

# Start metrics server on port 8001 (different from data_collector)
try:
    start_metrics_server(port=8001)
except Exception as e:
    logger.error(f"Failed to start metrics server: {str(e)}")


def detect_threats(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Analyze processed events to detect potential security threats.
    
    Args:
        events: List of processed and normalized events
        
    Returns:
        List of detected security alerts
    """
    alerts = []
    
    # Use the OperationTimer context manager for timing and metrics
    with OperationTimer("threat_detection"):
        try:
            # Group events by source IP for correlation
            ip_events = {}
            for event in events:
                source_ip = event.get('source_ip')
                if source_ip:
                    if source_ip not in ip_events:
                        ip_events[source_ip] = []
                    ip_events[source_ip].append(event)
            
            # Apply different detection rules
            auth_alerts = detect_authentication_attacks(events, ip_events)
            alerts.extend(auth_alerts)
            
            malware_alerts = detect_malware_indicators(events)
            alerts.extend(malware_alerts)
            
            network_alerts = detect_suspicious_network_activity(events, ip_events)
            alerts.extend(network_alerts)
            
            exfil_alerts = detect_data_exfiltration(events)
            alerts.extend(exfil_alerts)
            
            # Deduplicate alerts
            unique_alerts = deduplicate_alerts(alerts)
            
            # Prepare threat metrics by type and severity
            threat_types = {}
            for alert in unique_alerts:
                alert_type = alert.get('type', 'unknown')
                severity = alert.get('severity', 'medium')
                
                if alert_type not in threat_types:
                    threat_types[alert_type] = {}
                
                if severity not in threat_types[alert_type]:
                    threat_types[alert_type][severity] = 0
                    
                threat_types[alert_type][severity] += 1
            
            # Record threat detection metrics
            record_threat_detection(
                status="success",
                threats_count=len(unique_alerts),
                threat_types=threat_types
            )
            
            logger.info(f"Detected {len(unique_alerts)} unique security alerts")
            
            # Log summary of detected threats
            log_threat_event("detection_summary", "info", {
                "total_events_analyzed": len(events),
                "total_alerts_generated": len(alerts),
                "unique_alerts": len(unique_alerts),
                "auth_alerts": len(auth_alerts),
                "malware_alerts": len(malware_alerts),
                "network_alerts": len(network_alerts),
                "exfil_alerts": len(exfil_alerts)
            })
            
            return unique_alerts
        except Exception as e:
            log_error("threat_detection_error", str(e), {
                "events_count": len(events),
                "partial_alerts_count": len(alerts)
            })
            record_threat_detection(
                status="error",
                threats_count=0,
                threat_types={}
            )
            return []


def detect_authentication_attacks(events: List[Dict[str, Any]], ip_events: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """Detect authentication-related attacks like brute force attempts.
    
    Args:
        events: List of all processed events
        ip_events: Events grouped by source IP
        
    Returns:
        List of detected authentication attack alerts
    """
    alerts = []
    
    # Detect brute force attempts (multiple failed logins from same IP)
    for ip, ip_event_list in ip_events.items():
        # Filter for authentication events
        auth_events = [e for e in ip_event_list if e.get('event_type') == 'authentication']
        
        # Count failed authentication attempts
        failed_attempts = []
        for event in auth_events:
            # Look for indicators of failed authentication
            event_str = str(event).lower()
            if any(term in event_str for term in ['fail', 'invalid', 'bad password', 'incorrect', 'denied']):
                failed_attempts.append(event)
        
        # If multiple failed attempts are detected, create an alert
        if len(failed_attempts) >= 3:  # Threshold for brute force detection
            alerts.append({
                'alert_id': generate_alert_id(),
                'title': f"Potential brute force attack from {ip}",
                'description': f"Detected {len(failed_attempts)} failed authentication attempts from {ip}",
                'severity': 'high',
                'source_ip': ip,
                'event_type': 'authentication_attack',
                'created_at': datetime.now().isoformat(),
                'related_events': [e.get('event_id') for e in failed_attempts],
                'status': 'new'
            })
    
    return alerts


def detect_malware_indicators(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Detect indicators of malware activity in events.
    
    Args:
        events: List of processed events
        
    Returns:
        List of detected malware alerts
    """
    alerts = []
    
    # Simple keyword-based detection (in production, use more sophisticated methods)
    malware_indicators = [
        'malware', 'virus', 'trojan', 'ransomware', 'backdoor',
        'suspicious process', 'unauthorized execution', 'known bad file'
    ]
    
    for event in events:
        event_str = str(event).lower()
        
        # Check for malware indicators in event data
        for indicator in malware_indicators:
            if indicator in event_str:
                alerts.append({
                    'alert_id': generate_alert_id(),
                    'title': f"Potential malware detected: {indicator}",
                    'description': extract_description(event),
                    'severity': 'critical',
                    'source_ip': event.get('source_ip'),
                    'event_type': 'malware',
                    'created_at': datetime.now().isoformat(),
                    'related_events': [event.get('event_id')],
                    'status': 'new'
                })
                break  # Only create one alert per event
    
    return alerts


def detect_suspicious_network_activity(events: List[Dict[str, Any]], ip_events: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """Detect suspicious network activity patterns.
    
    Args:
        events: List of processed events
        ip_events: Events grouped by source IP
        
    Returns:
        List of detected network activity alerts
    """
    alerts = []
    
    # Detect port scanning (multiple connection attempts to different ports)
    for ip, ip_event_list in ip_events.items():
        # Extract port information from events
        ports = set()
        for event in ip_event_list:
            event_str = str(event).lower()
            if 'port' in event_str and event.get('event_type') == 'network':
                # This is a simplified approach - in production, extract actual port numbers
                ports.add(event_str)  # Using the event string as a proxy for port info
        
        # If connections to multiple ports are detected, create an alert
        if len(ports) >= 5:  # Threshold for port scan detection
            alerts.append({
                'alert_id': generate_alert_id(),
                'title': f"Potential port scanning from {ip}",
                'description': f"Detected connections to {len(ports)} different ports from {ip}",
                'severity': 'medium',
                'source_ip': ip,
                'event_type': 'network_scan',
                'created_at': datetime.now().isoformat(),
                'related_events': [e.get('event_id') for e in ip_event_list if 'port' in str(e).lower()],
                'status': 'new'
            })
    
    return alerts


def detect_data_exfiltration(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Detect potential data exfiltration attempts.
    
    Args:
        events: List of processed events
        
    Returns:
        List of detected data exfiltration alerts
    """
    alerts = []
    
    # Define thresholds for data exfiltration detection
    large_transfer_threshold = 10000000  # 10MB in bytes
    unusual_time_window = [22, 6]  # 10PM to 6AM
    sensitive_data_keywords = [
        'confidential', 'secret', 'classified', 'restricted', 'personal',
        'password', 'credit card', 'ssn', 'social security', 'database dump',
        'export', 'download', 'backup', 'extract'
    ]
    
    # Group events by source IP for correlation
    ip_events = {}
    for event in events:
        source_ip = event.get('source_ip')
        if source_ip:
            if source_ip not in ip_events:
                ip_events[source_ip] = []
            ip_events[source_ip].append(event)
    
    # Check for large outbound data transfers
    for event in events:
        if event.get('direction') == 'outbound' or event.get('traffic_direction') == 'outbound':
            # Check for large data transfers
            bytes_transferred = event.get('bytes_out', event.get('bytes', event.get('size', 0)))
            
            # Convert string values to integers if needed
            if isinstance(bytes_transferred, str):
                try:
                    bytes_transferred = int(bytes_transferred)
                except (ValueError, TypeError):
                    bytes_transferred = 0
            
            # Check if this is a large transfer
            if bytes_transferred > large_transfer_threshold:
                alerts.append({
                    'alert_id': generate_alert_id(),
                    'title': f"Large data transfer detected from {event.get('source_ip', 'unknown')}",
                    'description': f"Outbound transfer of {bytes_transferred} bytes to {event.get('destination_ip', 'unknown')}",
                    'severity': 'high',
                    'source_ip': event.get('source_ip'),
                    'destination_ip': event.get('destination_ip'),
                    'event_type': 'data_exfiltration',
                    'created_at': datetime.now().isoformat(),
                    'related_events': [event.get('event_id')],
                    'status': 'new',
                    'details': {
                        'bytes_transferred': bytes_transferred,
                        'protocol': event.get('protocol'),
                        'destination_port': event.get('destination_port')
                    }
                })
    
    # Check for transfers to unusual destinations
    known_domains = ['company.com', 'partner.org', 'vendor.net']  # Example trusted domains
    for event in events:
        destination = event.get('destination_domain', event.get('destination_host', ''))
        if destination and not any(domain in destination.lower() for domain in known_domains):
            # Check if there's data being transferred
            if event.get('bytes_out', 0) > 0 or event.get('bytes', 0) > 0:
                # Check if the event contains sensitive data keywords
                event_str = str(event).lower()
                if any(keyword in event_str for keyword in sensitive_data_keywords):
                    alerts.append({
                        'alert_id': generate_alert_id(),
                        'title': f"Potential data exfiltration to unusual destination",
                        'description': f"Sensitive data transfer detected to unusual destination: {destination}",
                        'severity': 'high',
                        'source_ip': event.get('source_ip'),
                        'destination_ip': event.get('destination_ip'),
                        'event_type': 'data_exfiltration',
                        'created_at': datetime.now().isoformat(),
                        'related_events': [event.get('event_id')],
                        'status': 'new',
                        'details': {
                            'destination': destination,
                            'sensitive_keywords': [k for k in sensitive_data_keywords if k in event_str]
                        }
                    })
    
    # Check for unusual timing of data transfers
    for event in events:
        if event.get('direction') == 'outbound' or event.get('traffic_direction') == 'outbound':
            # Check if timestamp is available
            timestamp = event.get('timestamp', event.get('created_at', ''))
            if timestamp:
                try:
                    # Try to parse the timestamp
                    if isinstance(timestamp, str):
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    else:
                        dt = timestamp
                    
                    # Check if the transfer occurred during unusual hours
                    hour = dt.hour
                    if unusual_time_window[0] <= hour or hour <= unusual_time_window[1]:  # 10PM to 6AM
                        # Check if there's significant data being transferred
                        bytes_transferred = event.get('bytes_out', event.get('bytes', event.get('size', 0)))
                        if bytes_transferred > 1000000:  # 1MB
                            alerts.append({
                                'alert_id': generate_alert_id(),
                                'title': f"After-hours data transfer detected",
                                'description': f"Large data transfer of {bytes_transferred} bytes detected during unusual hours ({hour}:00)",
                                'severity': 'medium',
                                'source_ip': event.get('source_ip'),
                                'destination_ip': event.get('destination_ip'),
                                'event_type': 'data_exfiltration',
                                'created_at': datetime.now().isoformat(),
                                'related_events': [event.get('event_id')],
                                'status': 'new',
                                'details': {
                                    'transfer_time': timestamp,
                                    'bytes_transferred': bytes_transferred
                                }
                            })
                except (ValueError, TypeError):
                    # Skip events with invalid timestamps
                    pass
    
    return alerts


def deduplicate_alerts(alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate alerts based on similar characteristics.
    
    Args:
        alerts: List of detected alerts
        
    Returns:
        List of unique alerts
    """
    if not alerts:
        return []
    
    # Group similar alerts
    alert_groups = {}
    for alert in alerts:
        # Create a key based on alert characteristics
        key = f"{alert['event_type']}:{alert.get('source_ip', 'unknown')}:{alert['severity']}"
        
        if key not in alert_groups:
            alert_groups[key] = []
        
        alert_groups[key].append(alert)
    
    # Take the most recent alert from each group
    unique_alerts = []
    for group in alert_groups.values():
        if len(group) == 1:
            unique_alerts.append(group[0])
        else:
            # Sort by creation time and take the most recent
            sorted_group = sorted(group, key=lambda x: x['created_at'], reverse=True)
            
            # Merge related events from all alerts in the group
            all_related_events = set()
            for alert in group:
                if 'related_events' in alert:
                    all_related_events.update(alert['related_events'])
            
            most_recent = sorted_group[0]
            most_recent['related_events'] = list(all_related_events)
            most_recent['description'] += f" ({len(group)} similar alerts merged)"
            
            unique_alerts.append(most_recent)
    
    return unique_alerts


def generate_alert_id() -> str:
    """Generate a unique ID for an alert.
    
    Returns:
        A unique alert ID string
    """
    import uuid
    return str(uuid.uuid4())


def extract_description(event: Dict[str, Any]) -> str:
    """Extract a description from an event for use in alerts.
    
    Args:
        event: The event to describe
        
    Returns:
        Description string
    """
    # Use the event's description if available
    if 'description' in event:
        return event['description']
    
    # Otherwise, create a description based on event type and source
    event_type = event.get('event_type', 'unknown')
    source = event.get('source', {}).get('name', 'unknown source')
    
    return f"Suspicious {event_type} activity detected from {source}"