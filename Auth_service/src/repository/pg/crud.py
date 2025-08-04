from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.pg.models import Clients
from src.services.security.hash_password import verify_password


async def create_user(email: str, password: str, uuid: str, db: AsyncSession) -> str:
    result = await db.execute(select(Clients).where(Clients.email == email))
    user_exists = result.scalar_one_or_none()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = Clients(
        email=email,
        hashed_password=password,
        uuid=uuid
    )
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user.uuid
    except Exception as e:
        await db.rollback()
        raise e

async def set_jti(uuid: str, jti: str, db: AsyncSession) -> None:
    result = await db.execute(select(Clients).where(Clients.uuid == uuid))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    try:
        client.jti = jti
        await db.commit()
        await db.refresh(client)
    except Exception as e:
        await db.rollback()
        raise e

async def get_user(email: str, password: str, db: AsyncSession) -> str :
    result = await db.execute(select(Clients).where(Clients.email == email))
    user_in_db = result.scalar_one_or_none()
    if not user_in_db:
        raise HTTPException(status_code=404, detail="User not found")
    password_verified = verify_password(password, user_in_db.hashed_password)
    if not password_verified:
        raise HTTPException(status_code=400, detail="Password incorrect")
    return user_in_db.uuid

async def verify_token_jti(payload: dict, db: AsyncSession) -> str:
    user_uuid = payload.get("sub")
    jti = payload.get("jti", None)
    if not jti:
        raise HTTPException(status_code=404, detail="JTI not found")
    result = await db.execute(select(Clients).where(Clients.uuid == user_uuid))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if jti != user.jti:
        raise HTTPException(status_code=401, detail="Refresh token incorrect")
    return user_uuid