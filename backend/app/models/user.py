from sqlalchemy import Boolean, Column, String, Integer, DateTime
from sqlalchemy.sql import func

from app.models.base import BaseModel


class User(BaseModel):
    """User model for authentication and authorization"""
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    
    # Security-related fields
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    last_login_attempt = Column(DateTime, nullable=True)
    account_locked_until = Column(DateTime, nullable=True)
    password_last_changed = Column(DateTime, default=func.now(), nullable=False)