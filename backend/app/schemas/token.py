from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Schema for access token"""
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None


class TokenPayload(BaseModel):
    """Schema for token payload"""
    sub: Optional[int] = None
    exp: Optional[int] = None