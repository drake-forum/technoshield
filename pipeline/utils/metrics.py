from prometheus_client import Counter, Histogram, Gauge, Summary, start_http_server
import time
from typing import Dict, Any, Optional
import threading
import logging

# Configure logger
logger = logging.getLogger(__name__)

# Define custom metrics
data_collection_total = Counter(
    "data_collection_total", 
    "Total number of data collection operations",
    ["source", "status"]
)

data_collection_duration = Histogram(
    "data_collection_duration_seconds", 
    "Data collection duration in seconds",
    ["source"],
    buckets=(0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0)
)

data_points_collected = Counter(
    "data_points_collected_total", 
    "Total number of data points collected",
    ["source", "data_type"]
)

threat_detection_total = Counter(
    "threat_detection_total", 
    "Total number of threat detection operations",
    ["status"]
)

threat_detection_duration = Histogram(
    "threat_detection_duration_seconds", 
    "Threat detection duration in seconds",
    buckets=(0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0)
)

threats_detected = Counter(
    "threats_detected_total", 
    "Total number of threats detected",
    ["type", "severity"]
)

processing_errors = Counter(
    "processing_errors_total", 
    "Total number of processing errors",
    ["component", "error_type"]
)

processing_queue_size = Gauge(
    "processing_queue_size", 
    "Current size of the processing queue"
)

data_freshness = Gauge(
    "data_freshness_seconds", 
    "Time since last data collection",
    ["source"]
)

# Metrics server state
_server_started = False
_server_lock = threading.Lock()


def start_metrics_server(port: int = 8000) -> None:
    """Start the Prometheus metrics HTTP server if not already running"""
    global _server_started
    
    with _server_lock:
        if not _server_started:
            try:
                start_http_server(port)
                _server_started = True
                logger.info(f"Started Prometheus metrics server on port {port}")
            except Exception as e:
                logger.error(f"Failed to start metrics server: {str(e)}")
                raise


# Context manager for timing operations
class OperationTimer:
    def __init__(self, operation_type: str, labels: Optional[Dict[str, str]] = None):
        self.operation_type = operation_type
        self.labels = labels or {}
        self.start_time = None
        
    def __enter__(self):
        self.start_time = time.time()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        
        if self.operation_type == "data_collection":
            data_collection_duration.labels(
                source=self.labels.get("source", "unknown")
            ).observe(duration)
        elif self.operation_type == "threat_detection":
            threat_detection_duration.observe(duration)


# Helper functions for recording metrics
def record_data_collection(source: str, status: str, data_points: int = 0, data_type: str = "unknown") -> None:
    """Record metrics for a data collection operation"""
    data_collection_total.labels(source=source, status=status).inc()
    
    if data_points > 0:
        data_points_collected.labels(source=source, data_type=data_type).inc(data_points)
    
    # Update data freshness timestamp
    if status == "success":
        data_freshness.labels(source=source).set(0)  # Reset to 0 when fresh data is collected


def record_threat_detection(status: str, threats_count: int = 0, threat_types: Dict[str, Dict[str, int]] = None) -> None:
    """Record metrics for a threat detection operation"""
    threat_detection_total.labels(status=status).inc()
    
    if threats_count > 0 and threat_types:
        for threat_type, severities in threat_types.items():
            for severity, count in severities.items():
                if count > 0:
                    threats_detected.labels(type=threat_type, severity=severity).inc(count)


def record_processing_error(component: str, error_type: str) -> None:
    """Record a processing error"""
    processing_errors.labels(component=component, error_type=error_type).inc()


def set_queue_size(size: int) -> None:
    """Set the current processing queue size"""
    processing_queue_size.set(size)


def update_data_freshness() -> None:
    """Update all data freshness metrics (should be called periodically)"""
    for source in ["api", "file", "syslog"]:
        try:
            # Get current value
            current = data_freshness.labels(source=source)._value.get()
            # Increment by the update interval (e.g., 60 seconds)
            if current is not None:  # Only update if the metric exists
                data_freshness.labels(source=source).set(current + 60)
        except Exception:
            # If the label doesn't exist yet, ignore
            pass