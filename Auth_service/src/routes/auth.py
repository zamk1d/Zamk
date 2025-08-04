"""Auth endpoints."""
from fastapi import APIRouter, Depends, Body, Response

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.config.cookie_settings import RefreshCookieSettings
from src.database.pg.async_session import get_db
from src.schemas.routes.auth.auth_schemas import LoginSchema, RegisterSchema
from src.schemas.routes.token.token_schemas import TokenResponseSchema, AccessTokenSchema
from src.services.auth import register, login
from src.services.send_code import send

auth = APIRouter(prefix="/auth", tags=["auth"])



@auth.post("/login", response_model=AccessTokenSchema)
async def login_user(
        data: Annotated[LoginSchema, Body()],
        response: Response,
        db: AsyncSession = Depends(get_db)
    ) -> AccessTokenSchema:
    """Validates response data and returns access + refresh tokens if data is valid"""

    tokens = await login(**data.model_dump(), db=db)
    response.set_cookie(
        value=tokens.refresh_token,
        **RefreshCookieSettings().model_dump()
    )
    return AccessTokenSchema(access_token=tokens.access_token)

@auth.post("/register", response_model=AccessTokenSchema, status_code=201)
async def register_user(
        data: Annotated[RegisterSchema, Body()],
        response: Response,
        db: AsyncSession = Depends(get_db)
) -> AccessTokenSchema:
    """Add new user if not exists to clients database"""

    tokens = await register(**data.model_dump(), db=db)
    response.set_cookie(
        value=tokens.refresh_token,
        **RefreshCookieSettings().model_dump()
    )
    return AccessTokenSchema(access_token=tokens.access_token)

@auth.post("/send_code", status_code=200)
async def send_code(email: Annotated[str, Body()]) -> dict:
    """Send code to email"""
    await send(email=email)
    return {"status": "ok"}