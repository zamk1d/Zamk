from random import randint
from src.database.redis_db.redis import save_code
from src.rabbitMQ.rabbit_handler import send_to_rabbitmq

async def send(email: str) -> None:
    code = randint(100000, 999999)
    try:
        await send_to_rabbitmq(queue_name="email_queue", message={"email": email, "code": code})
        await save_code(email, str(code))
    except Exception as e:
        raise e