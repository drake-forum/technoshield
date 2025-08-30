import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from pipeline.models.threat_detector import (
    detect_threats,
    detect_authentication_attacks,
    detect_malware_indicators,
    detect_suspicious_network_activity,
    detect_data_exfiltration
)


@pytest.fixture
def sample_network_data():
    # Create sample network data for testing
    current_time = datetime.now()
    return [
        {
            "timestamp": current_time - timedelta(minutes=5),
            "source_ip": "192.168.1.100",
            "destination_ip": "203.0.113.10",
            "bytes_sent": 5000000,  # 5MB
            "protocol": "TCP",
            "port": 443,
            "user": "user1"
        },
        {
            "timestamp": current_time - timedelta(minutes=10),
            "source_ip": "192.168.1.101",
            "destination_ip": "8.8.8.8",
            "bytes_sent": 2000,
            "protocol": "UDP",
            "port": 53,
            "user": "user2"
        },
        {
            "timestamp": current_time - timedelta(hours=3),  # Outside business hours
            "source_ip": "192.168.1.102",
            "destination_ip": "198.51.100.25",
            "bytes_sent": 8000000,  # 8MB
            "protocol": "TCP",
            "port": 22,
            "user": "user3"
        },
        {
            "timestamp": current_time - timedelta(minutes=15),
            "source_ip": "192.168.1.103",
            "destination_ip": "192.168.1.1",
            "bytes_sent": 1500,
            "protocol": "TCP",
            "port": 80,
            "user": "user4"
        },
        {
            "timestamp": current_time - timedelta(minutes=20),
            "source_ip": "192.168.1.104",
            "destination_ip": "192.0.2.123",  # Unusual destination
            "bytes_sent": 7000000,  # 7MB
            "protocol": "TCP",
            "port": 21,
            "user": "user5",
            "filename": "customer_data.xlsx"  # Sensitive data keyword
        }
    ]


def test_detect_data_exfiltration_large_transfer():
    # Test detection of large data transfers
    data = [
        {
            "timestamp": datetime.now(),
            "source_ip": "192.168.1.100",
            "destination_ip": "203.0.113.10",
            "bytes_sent": 15000000,  # 15MB (above threshold)
            "protocol": "TCP",
            "port": 443,
            "user": "user1"
        }
    ]
    
    alerts = detect_data_exfiltration(data)
    
    assert len(alerts) == 1
    assert "Large data transfer" in alerts[0]["description"]
    assert alerts[0]["severity"] == "high"


def test_detect_data_exfiltration_unusual_destination():
    # Test detection of transfers to unusual destinations with sensitive data keywords
    data = [
        {
            "timestamp": datetime.now(),
            "source_ip": "192.168.1.100",
            "destination_ip": "203.0.113.10",  # Unusual destination
            "bytes_sent": 5000000,  # 5MB
            "protocol": "TCP",
            "port": 443,
            "user": "user1",
            "filename": "passwords.txt"  # Sensitive data keyword
        }
    ]
    
    alerts = detect_data_exfiltration(data)
    
    assert len(alerts) == 1
    assert "Potential data exfiltration" in alerts[0]["description"]
    assert "sensitive data" in alerts[0]["description"]
    assert alerts[0]["severity"] == "high"


def test_detect_data_exfiltration_unusual_hours():
    # Test detection of large transfers during unusual hours
    # Set current time to 3 AM
    current_time = datetime.now().replace(hour=3, minute=0, second=0, microsecond=0)
    
    data = [
        {
            "timestamp": current_time,
            "source_ip": "192.168.1.100",
            "destination_ip": "203.0.113.10",
            "bytes_sent": 6000000,  # 6MB
            "protocol": "TCP",
            "port": 443,
            "user": "user1"
        }
    ]
    
    with patch('pipeline.models.threat_detector.datetime') as mock_datetime:
        mock_datetime.now.return_value = current_time
        alerts = detect_data_exfiltration(data)
    
    assert len(alerts) == 1
    assert "Unusual hours" in alerts[0]["description"]
    assert alerts[0]["severity"] == "medium"


def test_detect_data_exfiltration_multiple_criteria():
    # Test detection when multiple criteria are met
    # Set current time to 2 AM
    current_time = datetime.now().replace(hour=2, minute=0, second=0, microsecond=0)
    
    data = [
        {
            "timestamp": current_time,
            "source_ip": "192.168.1.100",
            "destination_ip": "203.0.113.10",  # Unusual destination
            "bytes_sent": 20000000,  # 20MB (above threshold)
            "protocol": "TCP",
            "port": 443,
            "user": "user1",
            "filename": "customer_database.sql"  # Sensitive data keyword
        }
    ]
    
    with patch('pipeline.models.threat_detector.datetime') as mock_datetime:
        mock_datetime.now.return_value = current_time
        alerts = detect_data_exfiltration(data)
    
    # Should generate multiple alerts or a higher severity alert
    assert len(alerts) >= 1
    # The first alert should be high severity
    assert alerts[0]["severity"] == "high"


def test_detect_data_exfiltration_no_alerts():
    # Test with normal data that shouldn't trigger alerts
    data = [
        {
            "timestamp": datetime.now(),
            "source_ip": "192.168.1.100",
            "destination_ip": "8.8.8.8",  # Common destination (Google DNS)
            "bytes_sent": 2000,  # Small transfer
            "protocol": "UDP",
            "port": 53,
            "user": "user1"
        }
    ]
    
    alerts = detect_data_exfiltration(data)
    
    assert len(alerts) == 0


def test_detect_data_exfiltration_with_sample_data(sample_network_data):
    # Test with the sample network data fixture
    alerts = detect_data_exfiltration(sample_network_data)
    
    # Should detect at least 2 suspicious activities:
    # 1. Large transfer outside business hours (8MB)
    # 2. Transfer of sensitive data to unusual destination (customer_data.xlsx)
    assert len(alerts) >= 2
    
    # Check that the alerts contain the expected descriptions
    alert_descriptions = [alert["description"] for alert in alerts]
    assert any("unusual hours" in desc.lower() for desc in alert_descriptions)
    assert any("sensitive data" in desc.lower() for desc in alert_descriptions)