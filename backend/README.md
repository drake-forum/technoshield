# TechnoShield Backend

This is the backend component of the TechnoShield Security Platform, built with FastAPI and SQLAlchemy.

## Directory Structure

```
backend/
├── app/                  # Main application package
│   ├── api/              # API endpoints
│   │   └── routes/       # Route definitions
│   ├── core/             # Core functionality
│   ├── db/               # Database configuration
│   ├── models/           # SQLAlchemy models
│   └── schemas/          # Pydantic schemas
├── tests/                # Test directory
└── requirements.txt      # Python dependencies
```

## Features

- **Authentication**: JWT-based authentication with refresh tokens
- **User Management**: User registration, profile management
- **Alert Management**: Create, update, and track security alerts
- **Incident Management**: Manage security incidents
- **Metrics**: Prometheus metrics for monitoring
- **Security**: HTTPS enforcement, rate limiting, password policies

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables (create a `.env` file in the backend directory):

```
API_V1_STR=/api/v1
PROJECT_NAME=TechnoShield
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
DATABASE_URI=postgresql://postgres:password@localhost:5432/technoshield
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
DATABASE_POOL_RECYCLE=3600
RATE_LIMIT_PER_MINUTE=60
```

4. Run the application:

```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests with pytest:

```bash
pytest
```

For test coverage:

```bash
pytest --cov=app tests/
```