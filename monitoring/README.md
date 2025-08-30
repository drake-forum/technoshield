# TECHNOSHIELD Monitoring and Logging Solution

This directory contains the configuration files for the monitoring and logging solution implemented for the TECHNOSHIELD cybersecurity platform.

## Components

### Logging

- **Structured Logging**: Both backend and pipeline components use structured logging with JSON formatting for machine-readable logs.
- **Log Rotation**: Implemented using Python's `RotatingFileHandler` to prevent log files from growing too large.
- **Log Levels**: Different log levels (INFO, ERROR) for different types of events.
- **Specialized Loggers**: Dedicated loggers for security events, errors, API requests, data collection, and threat detection.

### Metrics Collection

- **Prometheus**: Collects metrics from all services and stores them for querying.
- **Node Exporter**: Collects host-level metrics (CPU, memory, disk, network).
- **cAdvisor**: Collects container-level metrics.
- **Application Metrics**: Both backend and pipeline expose custom metrics endpoints.

### Visualization

- **Grafana**: Provides dashboards for visualizing metrics and monitoring system health.
- **Pre-configured Dashboards**: Includes dashboards for API performance, system resources, security alerts, and incidents.

## Accessing Monitoring Tools

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (default credentials: admin/admin)
- **Node Exporter Metrics**: http://localhost:9100/metrics
- **cAdvisor Metrics**: http://localhost:8081/metrics

## Key Metrics

### Backend API Metrics

- Request rate by endpoint
- Response time (95th percentile)
- Error rate
- Authentication success/failure rate

### Pipeline Metrics

- Data collection rate
- Threat detection time
- Alert generation rate
- Processing errors

### System Metrics

- CPU usage
- Memory usage
- Disk I/O
- Network traffic

## Log Files

### Backend Logs

- **Application Logs**: `logs/app.log`
- **Error Logs**: `logs/error.log`
- **Security Logs**: `logs/security.log`

### Pipeline Logs

- **Pipeline Logs**: `logs/pipeline.log`
- **Data Collection Logs**: `logs/data_collection.log`
- **Threat Detection Logs**: `logs/threat_detection.log`
- **Error Logs**: `logs/pipeline_error.log`

## Alerting

Alerts can be configured in Grafana based on metric thresholds. Common alert scenarios include:

- High error rate in API requests
- Slow response times
- Unusual number of security alerts
- System resource constraints (high CPU, memory, disk usage)

## Extending the Monitoring Solution

1. **Adding New Metrics**: Add new metrics to the application code using the Prometheus client libraries.
2. **Creating Custom Dashboards**: Import or create new dashboards in Grafana.
3. **Adding Alert Rules**: Configure alert rules in Grafana or Prometheus.
4. **Log Analysis**: Consider adding ELK stack (Elasticsearch, Logstash, Kibana) for advanced log analysis.