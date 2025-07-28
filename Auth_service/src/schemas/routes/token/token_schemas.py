"""Tokens schemas."""
from pydantic import BaseModel, EmailStr, Field

class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str

class AccessTokenSchema(BaseModel):
    access_token: str