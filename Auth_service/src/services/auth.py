"""Business logic of auth endpoints."""
from fastapi import HTTPException
from sqlalchemy import select
from uuid import uuid4

from src.repository.pg.crud import create_user, set_jti, get_user
from src.schemas.routes.token.token_schemas import TokenResponseSchema
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.pg.models import Clients
from src.services.security.hash_password import hash_password
from src.services.security.token_signature import create_jwt


async def login(email: str, password: str, db: AsyncSession) -> TokenResponseSchema:
    """business-logic of /login endpoint."""
    user_uuid = await get_user(email=email, password=password, db=db)

    payload = {"sub": user_uuid}
    tokens = create_jwt(payload=payload)

    await set_jti(uuid=user_uuid, jti=tokens.get("jti"), db=db)

    return TokenResponseSchema(access_token=tokens.get("at"), refresh_token=tokens.get("rt"))

async def register(email: str, password: str, db: AsyncSession) -> TokenResponseSchema:
    """business-logic of /register endpoint."""
    user_uuid = await create_user(email=email, password=hash_password(password), uuid=str(uuid4()), db=db)

    payload = {"sub": user_uuid}
    tokens = create_jwt(payload=payload)

    await set_jti(uuid=user_uuid, jti=tokens.get("jti"), db=db)

    return TokenResponseSchema(access_token=tokens.get("at"), refresh_token=tokens.get("rt"))