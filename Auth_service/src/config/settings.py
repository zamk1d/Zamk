"""Env settings."""
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv(os.path.join("..",".env"))

class Settings(BaseSettings):
    DATABASE_URL: str = None

    class Config:
        env_file = ".env"

settings = Settings()