import json
from backend.db.resdis import redis_client


# 🔑 Get value from cache
async def get_cache(key: str):
    try:
        value = await redis_client.get(key)

        if value:
            return json.loads(value)

        return None

    except Exception as e:
        print(f"❌ Redis GET error: {e}")
        return None


# 💾 Set value in cache
async def set_cache(key: str, value: dict, ttl: int = 3600):
    try:
        await redis_client.set(
            key,
            json.dumps(value),
            ex=ttl  # expiry in seconds
        )

    except Exception as e:
        print(f"❌ Redis SET error: {e}")


# ❌ Delete cache
async def delete_cache(key: str):
    try:
        await redis_client.delete(key)

    except Exception as e:
        print(f"❌ Redis DELETE error: {e}")


# 🧪 Test Redis
async def test_redis():
    try:
        await redis_client.set("test_key", "hello_redis")
        value = await redis_client.get("test_key")

        print("✅ Redis working:", value)

        return value

    except Exception as e:
        print(f"❌ Redis error: {e}")
        return None