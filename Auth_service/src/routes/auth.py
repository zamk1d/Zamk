"""Auth endpoints."""
from fastapi import APIRouter, Depends, Body, Response

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.config.cookie_settings import RefreshCookieSettings
from src.database.pg.async_session import get_db
from src.schemas.routes.auth.auth_schemas import LoginSchema, RegisterSchema
from src.schemas.routes.token.token_schemas import TokenResponseSchema, AccessTokenSchema

auth = APIRouter(prefix="/auth", tags=["auth"])



@auth.post("/login", response_model=AccessTokenSchema)
async def login_user(
        data: Annotated[LoginSchema, Body()],
        response: Response,
        db: AsyncSession = Depends(get_db)
    ) -> AccessTokenSchema:

    """Validates response data and returns access + refresh tokens if data is valid"""

    # db method

    tokens = TokenResponseSchema(access_token="123", refresh_token="456")
    response.set_cookie(
        value=tokens.refresh_token,
        **RefreshCookieSettings().model_dump()
    )
    return AccessTokenSchema(access_token=tokens.access_token)

@auth.post("/register", response_model=AccessTokenSchema)
async def register_user(
        data: Annotated[RegisterSchema, Body()],
        response: Response,
        db: AsyncSession = Depends(get_db)
    ) -> AccessTokenSchema:
    """Add new user if not exists to clients database"""

    # db method

    tokens = TokenResponseSchema(access_token="123", refresh_token="456")
    response.set_cookie(
        value=tokens.refresh_token,
        **RefreshCookieSettings().model_dump()
    )
    return AccessTokenSchema(access_token=tokens.access_token)
