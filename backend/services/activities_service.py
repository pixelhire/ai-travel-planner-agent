import asyncio
from backend.db.postgres_db import init_db
from backend.services.db_service import test_db_connection


def testing_connection():
    print("Sending db call to test:")

    # run async code inside sync function
    rows = asyncio.run(run_test())

    print("Result from db:", rows)


async def run_test():
    # 🔥 IMPORTANT: initialize DB first
    await init_db()

    # call your async method
    rows = await test_db_connection()

    return rows