"""Token endpoints."""
from fastapi import APIRouter, Depends, Cookie, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.config.cookie_settings import RefreshCookieSettings
from src.database.pg.async_session import get_db
from fastapi.security import OAuth2PasswordBearer

from src.schemas.routes.token.token_schemas import AccessTokenSchema
from src.services.security.token_signature import verify_token
from src.services.token import refresh

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

token = APIRouter(prefix="/tokens", tags=["tokens"])

@token.get("/refresh", response_model=AccessTokenSchema)
async def refresh_tokens(
        refresh_token: Annotated[str, Cookie()],
        response: Response,
        db: AsyncSession = Depends(get_db)
) -> AccessTokenSchema:
    """Validates user refresh token from cookie and return access + refresh tokens"""

    tokens = await refresh(refresh_token=refresh_token, db=db)
    response.set_cookie(
        value=tokens.refresh_token,
        **RefreshCookieSettings().model_dump()
    )
    return AccessTokenSchema(access_token=tokens.access_token)