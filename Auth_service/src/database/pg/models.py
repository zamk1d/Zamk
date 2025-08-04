"""Database table model."""

from sqlalchemy import Table, Integer, String, Column, ForeignKey, Boolean, DateTime
from src.database.pg.base import Base
import uuid

class Clients(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    jti = Column(String, unique=True)
    uuid = Column(String, unique=True, nullable=False, default=str(uuid.uuid4), index=True)