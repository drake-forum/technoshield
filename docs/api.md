# TECHNOSHIELD API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

### Login

```
POST /auth/login
```

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Register

```
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2023-01-01T00:00:00"
}
```

## Users

### Get Current User

```
GET /users/me
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

### Update Current User

```
PUT /users/me
```

**Request Body:**
```json
{
  "full_name": "John Smith",
  "password": "newpassword123"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Smith",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-02T00:00:00"
}
```

### Get Users (Admin Only)

```
GET /users/
```

**Response:**
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Smith",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-02T00:00:00"
  },
  {
    "id": 2,
    "email": "admin@example.com",
    "full_name": "Admin User",
    "is_active": true,
    "is_superuser": true,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
  }
]
```

## Dashboard

### Get Dashboard Summary

```
GET /dashboard/summary
```

**Response:**
```json
{
  "alerts": {
    "total": 120,
    "by_severity": {
      "low": 45,
      "medium": 38,
      "high": 27,
      "critical": 10
    },
    "by_status": {
      "new": 25,
      "investigating": 15,
      "resolved": 70,
      "false_positive": 10
    }
  },
  "incidents": {
    "total": 35,
    "by_status": {
      "open": 8,
      "investigating": 12,
      "contained": 5,
      "eradicated": 3,
      "recovered": 2,
      "closed": 5
    }
  },
  "users": {
    "total": 15
  }
}
```

### Get Threat Map Data

```
GET /dashboard/threat-map
```

**Response:**
```json
{
  "locations": [
    {
      "latitude": 40.7128,
      "longitude": -74.0060,
      "severity": "critical",
      "count": 5
    },
    {
      "latitude": 34.0522,
      "longitude": -118.2437,
      "severity": "high",
      "count": 3
    },
    {
      "latitude": 51.5074,
      "longitude": -0.1278,
      "severity": "medium",
      "count": 7
    }
  ]
}
```

## Alerts

### Get Alerts

```
GET /alerts/
```

**Query Parameters:**
- `skip`: Number of items to skip (default: 0)
- `limit`: Maximum number of items to return (default: 100)
- `severity`: Filter by severity (optional)
- `status`: Filter by status (optional)

**Response:**
```json
[
  {
    "id": 1,
    "title": "Suspicious Login Attempt",
    "description": "Multiple failed login attempts from IP 192.168.1.100",
    "source": "auth-service",
    "severity": "high",
    "status": "investigating",
    "created_at": "2023-01-01T12:34:56",
    "updated_at": "2023-01-01T13:00:00",
    "assigned_to_id": 1,
    "incident_id": null
  },
  {
    "id": 2,
    "title": "Malware Detected",
    "description": "Malicious file detected on workstation WS-001",
    "source": "endpoint-protection",
    "severity": "critical",
    "status": "new",
    "created_at": "2023-01-01T14:22:33",
    "updated_at": null,
    "assigned_to_id": null,
    "incident_id": null
  }
]
```

### Get Alert by ID

```
GET /alerts/{alert_id}
```

**Response:**
```json
{
  "id": 1,
  "title": "Suspicious Login Attempt",
  "description": "Multiple failed login attempts from IP 192.168.1.100",
  "source": "auth-service",
  "severity": "high",
  "status": "investigating",
  "created_at": "2023-01-01T12:34:56",
  "updated_at": "2023-01-01T13:00:00",
  "assigned_to_id": 1,
  "incident_id": null
}
```

### Create Alert

```
POST /alerts/
```

**Request Body:**
```json
{
  "title": "Suspicious Network Traffic",
  "description": "Unusual outbound traffic to IP 203.0.113.100",
  "source": "network-monitor",
  "severity": "medium"
}
```

**Response:**
```json
{
  "id": 3,
  "title": "Suspicious Network Traffic",
  "description": "Unusual outbound traffic to IP 203.0.113.100",
  "source": "network-monitor",
  "severity": "medium",
  "status": "new",
  "created_at": "2023-01-02T09:45:12",
  "updated_at": null,
  "assigned_to_id": null,
  "incident_id": null
}
```

### Update Alert

```
PUT /alerts/{alert_id}
```

**Request Body:**
```json
{
  "status": "resolved",
  "assigned_to_id": 1
}
```

**Response:**
```json
{
  "id": 3,
  "title": "Suspicious Network Traffic",
  "description": "Unusual outbound traffic to IP 203.0.113.100",
  "source": "network-monitor",
  "severity": "medium",
  "status": "resolved",
  "created_at": "2023-01-02T09:45:12",
  "updated_at": "2023-01-02T10:15:30",
  "assigned_to_id": 1,
  "incident_id": null
}
```

## Incidents

### Get Incidents

```
GET /incidents/
```

**Query Parameters:**
- `skip`: Number of items to skip (default: 0)
- `limit`: Maximum number of items to return (default: 100)
- `severity`: Filter by severity (optional)
- `status`: Filter by status (optional)

**Response:**
```json
[
  {
    "id": 1,
    "title": "Ransomware Attack",
    "description": "Ransomware detected on multiple systems",
    "severity": "critical",
    "status": "investigating",
    "created_at": "2023-01-01T15:30:00",
    "updated_at": "2023-01-01T16:45:00",
    "resolved_at": null,
    "assigned_to_id": 1,
    "alerts": [
      {
        "id": 4,
        "title": "Ransomware Signature Detected",
        "description": "Ransomware signature detected on file server",
        "source": "antivirus",
        "severity": "critical",
        "status": "investigating",
        "created_at": "2023-01-01T15:25:00",
        "updated_at": "2023-01-01T15:30:00",
        "assigned_to_id": 1,
        "incident_id": 1
      }
    ]
  }
]
```

### Get Incident by ID

```
GET /incidents/{incident_id}
```

**Response:**
```json
{
  "id": 1,
  "title": "Ransomware Attack",
  "description": "Ransomware detected on multiple systems",
  "severity": "critical",
  "status": "investigating",
  "created_at": "2023-01-01T15:30:00",
  "updated_at": "2023-01-01T16:45:00",
  "resolved_at": null,
  "assigned_to_id": 1,
  "alerts": [
    {
      "id": 4,
      "title": "Ransomware Signature Detected",
      "description": "Ransomware signature detected on file server",
      "source": "antivirus",
      "severity": "critical",
      "status": "investigating",
      "created_at": "2023-01-01T15:25:00",
      "updated_at": "2023-01-01T15:30:00",
      "assigned_to_id": 1,
      "incident_id": 1
    }
  ]
}
```

### Create Incident

```
POST /incidents/
```

**Request Body:**
```json
{
  "title": "Data Breach Investigation",
  "description": "Potential data breach from web application",
  "severity": "high",
  "assigned_to_id": 1
}
```

**Response:**
```json
{
  "id": 2,
  "title": "Data Breach Investigation",
  "description": "Potential data breach from web application",
  "severity": "high",
  "status": "open",
  "created_at": "2023-01-02T11:20:00",
  "updated_at": null,
  "resolved_at": null,
  "assigned_to_id": 1,
  "alerts": []
}
```

### Update Incident

```
PUT /incidents/{incident_id}
```

**Request Body:**
```json
{
  "status": "contained",
  "description": "Potential data breach from web application. Initial containment measures applied."
}
```

**Response:**
```json
{
  "id": 2,
  "title": "Data Breach Investigation",
  "description": "Potential data breach from web application. Initial containment measures applied.",
  "severity": "high",
  "status": "contained",
  "created_at": "2023-01-02T11:20:00",
  "updated_at": "2023-01-02T14:30:00",
  "resolved_at": null,
  "assigned_to_id": 1,
  "alerts": []
}
```

### Add Alert to Incident

```
POST /incidents/{incident_id}/alerts
```

**Request Body:**
```json
{
  "alert_id": 5
}
```

**Response:**
```json
{
  "id": 2,
  "title": "Data Breach Investigation",
  "description": "Potential data breach from web application. Initial containment measures applied.",
  "severity": "high",
  "status": "contained",
  "created_at": "2023-01-02T11:20:00",
  "updated_at": "2023-01-02T14:35:00",
  "resolved_at": null,
  "assigned_to_id": 1,
  "alerts": [
    {
      "id": 5,
      "title": "Suspicious Database Query",
      "description": "Unusual database query pattern detected",
      "source": "database-monitor",
      "severity": "high",
      "status": "investigating",
      "created_at": "2023-01-02T11:15:00",
      "updated_at": "2023-01-02T14:35:00",
      "assigned_to_id": 1,
      "incident_id": 2
    }
  ]
}
```

## Reports

### Get Security Summary Report

```
GET /reports/security-summary
```

**Query Parameters:**
- `start_date`: Start date for report (format: YYYY-MM-DD)
- `end_date`: End date for report (format: YYYY-MM-DD)

**Response:**
```json
{
  "period": {
    "start_date": "2023-01-01",
    "end_date": "2023-01-31"
  },
  "alerts": {
    "total": 245,
    "by_severity": {
      "low": 98,
      "medium": 87,
      "high": 45,
      "critical": 15
    },
    "by_status": {
      "new": 35,
      "investigating": 42,
      "resolved": 158,
      "false_positive": 10
    }
  },
  "incidents": {
    "total": 28,
    "by_severity": {
      "low": 8,
      "medium": 12,
      "high": 6,
      "critical": 2
    },
    "by_status": {
      "open": 5,
      "investigating": 8,
      "contained": 4,
      "eradicated": 3,
      "recovered": 3,
      "closed": 5
    },
    "avg_time_to_resolution": "18:45:22"
  }
}
```

### Get Alert Trends Report

```
GET /reports/alert-trends
```

**Query Parameters:**
- `start_date`: Start date for report (format: YYYY-MM-DD)
- `end_date`: End date for report (format: YYYY-MM-DD)
- `interval`: Grouping interval (daily, weekly, monthly)

**Response:**
```json
{
  "period": {
    "start_date": "2023-01-01",
    "end_date": "2023-01-31",
    "interval": "daily"
  },
  "trends": [
    {
      "date": "2023-01-01",
      "total": 8,
      "by_severity": {
        "low": 3,
        "medium": 3,
        "high": 2,
        "critical": 0
      }
    },
    {
      "date": "2023-01-02",
      "total": 12,
      "by_severity": {
        "low": 5,
        "medium": 4,
        "high": 2,
        "critical": 1
      }
    }
  ]
}
```

### Get Incident Response Report

```
GET /reports/incident-response
```

**Query Parameters:**
- `start_date`: Start date for report (format: YYYY-MM-DD)
- `end_date`: End date for report (format: YYYY-MM-DD)

**Response:**
```json
{
  "period": {
    "start_date": "2023-01-01",
    "end_date": "2023-01-31"
  },
  "metrics": {
    "total_incidents": 28,
    "avg_time_to_detection": "00:45:18",
    "avg_time_to_containment": "04:12:33",
    "avg_time_to_eradication": "12:30:45",
    "avg_time_to_recovery": "18:45:22",
    "avg_time_to_resolution": "26:15:40"
  },
  "incidents_by_severity": {
    "low": {
      "count": 8,
      "avg_resolution_time": "12:30:15"
    },
    "medium": {
      "count": 12,
      "avg_resolution_time": "18:45:30"
    },
    "high": {
      "count": 6,
      "avg_resolution_time": "36:20:10"
    },
    "critical": {
      "count": 2,
      "avg_resolution_time": "72:15:45"
    }
  }
}
```