"""Env settings."""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    RABBIT_URL: str
    att: int = 15
    rtt: int = 7

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()