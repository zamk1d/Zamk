"""Cookie settings."""

from typing import Literal

from pydantic import BaseModel

class CommonCookieSettings(BaseModel):
    max_age: int =60*60*24*7
    httponly: bool = True
    samesite: Literal["lax", "strict", "none"] = "lax"
    secure: bool = False

class RefreshCookieSettings(CommonCookieSettings):
    key: str = "refresh_token"