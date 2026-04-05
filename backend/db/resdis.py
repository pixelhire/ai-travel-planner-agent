import redis.asyncio as redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.from_url(os.getenv("REDIS_URL"))


async def init_redis():
    await redis_client.ping()  # ensures connection