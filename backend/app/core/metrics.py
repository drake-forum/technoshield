from prometheus_client import Counter, Histogram, Gauge
import time

# Request metrics
HTTP_REQUEST_COUNTER = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status']
)

HTTP_REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# Authentication metrics
AUTH_SUCCESS_COUNTER = Counter(
    'auth_success_total',
    'Total number of successful authentication attempts',
    ['method']
)

AUTH_FAILURE_COUNTER = Counter(
    'auth_failure_total',
    'Total number of failed authentication attempts',
    ['method', 'reason']
)

# Alert metrics
ALERT_COUNTER = Counter(
    'alerts_total',
    'Total number of security alerts',
    ['severity', 'type']
)

ACTIVE_ALERTS_GAUGE = Gauge(
    'active_alerts',
    'Number of active security alerts',
    ['severity']
)

# Incident metrics
INCIDENT_COUNTER = Counter(
    'incidents_total',
    'Total number of security incidents',
    ['severity', 'status']
)

ACTIVE_INCIDENTS_GAUGE = Gauge(
    'active_incidents',
    'Number of active security incidents',
    ['severity']
)

# API rate limiting metrics
RATE_LIMIT_COUNTER = Counter(
    'rate_limit_hits_total',
    'Total number of rate limit hits',
    ['endpoint']
)


def record_request_metrics(method, endpoint, status, duration):
    """Record metrics for an HTTP request"""
    HTTP_REQUEST_COUNTER.labels(method=method, endpoint=endpoint, status=status).inc()
    HTTP_REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)


def record_auth_success(method='password'):
    """Record a successful authentication"""
    AUTH_SUCCESS_COUNTER.labels(method=method).inc()


def record_auth_failure(reason, method='password'):
    """Record a failed authentication"""
    AUTH_FAILURE_COUNTER.labels(method=method, reason=reason).inc()


def record_alert(severity, alert_type):
    """Record a security alert"""
    ALERT_COUNTER.labels(severity=severity, type=alert_type).inc()
    ACTIVE_ALERTS_GAUGE.labels(severity=severity).inc()


def resolve_alert(severity):
    """Mark an alert as resolved"""
    ACTIVE_ALERTS_GAUGE.labels(severity=severity).dec()


def record_incident(severity, status):
    """Record a security incident"""
    INCIDENT_COUNTER.labels(severity=severity, status=status).inc()
    if status in ['new', 'investigating']:
        ACTIVE_INCIDENTS_GAUGE.labels(severity=severity).inc()


def resolve_incident(severity):
    """Mark an incident as resolved"""
    ACTIVE_INCIDENTS_GAUGE.labels(severity=severity).dec()


def record_rate_limit_hit(endpoint):
    """Record a rate limit hit"""
    RATE_LIMIT_COUNTER.labels(endpoint=endpoint).inc()