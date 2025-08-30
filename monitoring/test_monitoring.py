#!/usr/bin/env python3

import requests
import time
import random
import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import metrics functions
from backend.app.core.metrics import record_alert, record_incident, record_auth_failure
from pipeline.utils.metrics import record_data_collection, record_threat_detection


def test_backend_metrics():
    """Generate test metrics for the backend"""
    print("Generating backend metrics...")
    
    # Generate alerts with different severities and types
    alert_types = ["malware", "intrusion", "anomaly", "policy_violation"]
    severities = ["critical", "high", "medium", "low"]
    
    for _ in range(20):
        alert_type = random.choice(alert_types)
        severity = random.choice(severities)
        record_alert(severity, alert_type)
        print(f"Recorded alert: {severity} {alert_type}")
        time.sleep(0.5)
    
    # Generate incidents
    statuses = ["new", "investigating", "resolved"]
    
    for _ in range(10):
        severity = random.choice(severities)
        status = random.choice(statuses)
        record_incident(severity, status)
        print(f"Recorded incident: {severity} {status}")
        time.sleep(0.5)
    
    # Generate auth failures
    reasons = ["invalid_credentials", "expired_token", "insufficient_permissions", "account_locked"]
    
    for _ in range(15):
        reason = random.choice(reasons)
        record_auth_failure(reason)
        print(f"Recorded auth failure: {reason}")
        time.sleep(0.5)


def test_pipeline_metrics():
    """Generate test metrics for the pipeline"""
    print("\nGenerating pipeline metrics...")
    
    # Generate data collection metrics
    sources = ["api", "file", "syslog"]
    data_types = ["logs", "events", "alerts", "telemetry"]
    
    for _ in range(15):
        source = random.choice(sources)
        data_type = random.choice(data_types)
        status = "success" if random.random() > 0.2 else "error"
        data_points = random.randint(10, 1000) if status == "success" else 0
        
        record_data_collection(
            source=source,
            status=status,
            data_points=data_points,
            data_type=data_type
        )
        print(f"Recorded data collection: {source} {status} {data_points} points")
        time.sleep(0.5)
    
    # Generate threat detection metrics
    threat_types = {
        "authentication_attack": {"high": 5, "medium": 8, "low": 3},
        "malware": {"critical": 2, "high": 7},
        "network_scan": {"medium": 12, "low": 9},
        "data_exfiltration": {"critical": 1, "high": 3}
    }
    
    record_threat_detection(
        status="success",
        threats_count=50,
        threat_types=threat_types
    )
    print(f"Recorded threat detection with 50 threats")


def check_prometheus():
    """Check if Prometheus is accessible"""
    try:
        response = requests.get("http://localhost:9090/-/healthy")
        if response.status_code == 200:
            print("\nPrometheus is running and healthy")
        else:
            print(f"\nPrometheus returned status code {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("\nCould not connect to Prometheus. Make sure it's running.")


def check_grafana():
    """Check if Grafana is accessible"""
    try:
        response = requests.get("http://localhost:3000/api/health")
        if response.status_code == 200:
            print("Grafana is running and healthy")
        else:
            print(f"Grafana returned status code {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to Grafana. Make sure it's running.")


if __name__ == "__main__":
    print("TECHNOSHIELD Monitoring Test Script")
    print("=================================")
    
    # Check if monitoring services are running
    check_prometheus()
    check_grafana()
    
    # Ask user if they want to generate test metrics
    choice = input("\nDo you want to generate test metrics? (y/n): ")
    
    if choice.lower() == 'y':
        test_backend_metrics()
        test_pipeline_metrics()
        print("\nTest metrics generation complete!")
        print("Check Grafana dashboards to see the results.")
    else:
        print("\nExiting without generating test metrics.")