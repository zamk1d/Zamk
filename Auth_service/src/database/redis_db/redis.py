import asyncio
from redis.asyncio import Redis

redis = Redis(host="localhost", port=6379, decode_responses=True)

async def save_code(email: str, code: str):
    key = f"verify_code:{email}"
    await redis.set(key, code, ex=300)  # 5 минут

async def check_code(email: str, input_code: str) -> bool:
    key = f"verify_code:{email}"
    stored_code = await redis.get(key)
    return stored_code == input_code
