"""Business logic of token endpoints."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.pg.crud import set_jti, verify_token_jti
from src.schemas.routes.token.token_schemas import TokenResponseSchema
from src.services.security.token_signature import create_jwt, verify_token


async def refresh(refresh_token: str, db: AsyncSession) -> TokenResponseSchema:
    """Refresh_both_tokens"""
    payload = verify_token(token=refresh_token)
    user_uuid = await verify_token_jti(payload=payload, db=db)
    payload = {"sub": user_uuid}
    tokens = create_jwt(payload=payload)

    await set_jti(uuid=user_uuid, jti=tokens.get("jti"), db=db)

    return TokenResponseSchema(access_token=tokens.get("at"), refresh_token=tokens.get("rt"))