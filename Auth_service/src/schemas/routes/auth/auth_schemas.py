"""Schemas for auth endpoints."""
from pydantic import BaseModel, EmailStr, Field


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class RegisterSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=5, max_length=64)
    code: str
