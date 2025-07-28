"""Main file"""
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.routes.auth import auth
from src.routes.token import token

from src.database.pg.init_db import init_db

@asynccontextmanager
async def startup_event(app: FastAPI):
    await init_db()
    yield

app = FastAPI()
app.include_router(auth)
app.include_router(token)


