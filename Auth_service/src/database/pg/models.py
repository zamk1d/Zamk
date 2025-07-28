"""Database table model."""

from sqlalchemy import Table, Integer, String, Column, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Clients(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    refresh_token = Column(String)
    uuid = Column(String, unique=True, nullable=False)