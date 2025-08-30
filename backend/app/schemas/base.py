from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    """Base schema with common fields"""
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class BaseResponseSchema(BaseSchema):
    """Base schema for response models"""
    id: int
    created_at: datetime
    updated_at: datetime