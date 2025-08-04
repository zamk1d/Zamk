"""Main file"""
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.routes.auth import auth
from src.routes.token import token
from src.database.pg.drop_init_func import init_db
from src.rabbitMQ.rabbit_handler import consume_messages

@asynccontextmanager
async def startup_event(app: FastAPI):
    # await init_db()
    asyncio.create_task(consume_messages(queue_name="auth_queue"))
    yield

app = FastAPI(lifespan=startup_event)
app.include_router(auth)
app.include_router(token)
