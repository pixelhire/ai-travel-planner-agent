import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

_db_pool = None


# 🔌 Initialize DB
async def init_db():
    global _db_pool

    try:
        _db_pool = await asyncpg.create_pool(
            dsn=os.getenv("DATABASE_URL")
        )
        print("✅ PostgreSQL connected")

    except Exception as e:
        print(f"❌ DB not running or connection failed: {e}")
        _db_pool = None
        # raise Exception("Database initialization failed")


# 🔁 Get DB pool safely
def get_db():
    if _db_pool is None:
        raise Exception("❌ DB not initialized. Is PostgreSQL running?")
    return _db_pool