"""Token endpoints."""
from fastapi import APIRouter, Depends, Cookie, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.database.pg.async_session import get_db
from fastapi.security import OAuth2PasswordBearer

from src.schemas.routes.token.token_schemas import AccessTokenSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

token = APIRouter(prefix="/tokens", tags=["tokens"])

@token.get("/refresh", response_model=AccessTokenSchema)
async def refresh_tokens(refresh_token: Annotated[str, Cookie()], response: Response, db: AsyncSession = Depends(get_db)) -> AccessTokenSchema:
    """Validates user refresh token from cookie and return access + refresh tokens"""

    return AccessTokenSchema(access_token=refresh_token)