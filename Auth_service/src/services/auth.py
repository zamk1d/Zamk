"""Business logic of auth endpoints."""
from src.schemas.routes.token.token_schemas import AccessTokenSchema


async def login(email: str, password: str) -> AccessTokenSchema:
    """business-logic of /login endpoint."""

    pass

async def register(email: str, password: str) -> AccessTokenSchema:
    """business-logic of /register endpoint."""

    pass

