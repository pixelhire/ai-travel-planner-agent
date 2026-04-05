from typing import Optional
from backend.db.postgres_db import get_db


# 🔍 Get itinerary by hash
async def get_itinerary_by_hash(input_hash: str):
    db = get_db()
    try:
        query = """
            SELECT * FROM itineraries
            WHERE input_hash = $1
        """
        return await db.fetchrow(query, input_hash)

    except Exception as e:
        print(f"❌ get_itinerary_by_hash error: {e}")
        return None


# ➕ Insert itinerary
async def insert_itinerary(input_hash: str, input_json: dict, output_json: dict):
    db = get_db()
    try:
        query = """
            INSERT INTO itineraries (input_hash, input_json, output_json)
            VALUES ($1, $2, $3)
            RETURNING *
        """
        return await db.fetchrow(query, input_hash, input_json, output_json)

    except Exception as e:
        print(f"❌ insert_itinerary error: {e}")
        return None


# 🔄 Update usage count
async def increment_itinerary_usage(itinerary_id: str):
    db = get_db()
    try:
        query = """
            UPDATE itineraries
            SET usage_count = usage_count + 1
            WHERE id = $1
        """
        await db.execute(query, itinerary_id)

    except Exception as e:
        print(f"❌ increment_itinerary_usage error: {e}")


# 🧾 Create user trip
async def create_user_trip(user_id: str, itinerary_id: str, trip_name: Optional[str] = None):
    db = get_db()
    try:
        query = """
            INSERT INTO user_trips (user_id, itinerary_id, trip_name)
            VALUES ($1, $2, $3)
            RETURNING *
        """
        return await db.fetchrow(query, user_id, itinerary_id, trip_name)

    except Exception as e:
        print(f"❌ create_user_trip error: {e}")
        return None


# ✏️ Update custom trip
async def update_user_trip(trip_id: str, custom_json: dict):
    db = get_db()
    try:
        query = """
            UPDATE user_trips
            SET custom_json = $1,
                is_modified = TRUE,
                version = version + 1
            WHERE id = $2
            RETURNING *
        """
        return await db.fetchrow(query, custom_json, trip_id)

    except Exception as e:
        print(f"❌ update_user_trip error: {e}")
        return None


# 🔍 Get user trips
async def get_user_trips(user_id: str):
    db = get_db()
    try:
        query = """
            SELECT * FROM user_trips
            WHERE user_id = $1
            ORDER BY created_at DESC
        """
        return await db.fetch(query, user_id)

    except Exception as e:
        print(f"❌ get_user_trips error: {e}")
        return []


# 📊 Log search
async def log_search(user_id: str, input_hash: str, raw_query: str, input_json: dict, itinerary_id: str, status: str):
    db = get_db()
    try:
        query = """
            INSERT INTO search_logs (user_id, input_hash, raw_query, input_json, itinerary_id, status)
            VALUES ($1, $2, $3, $4, $5, $6)
        """
        await db.execute(query, user_id, input_hash, raw_query, input_json, itinerary_id, status)

    except Exception as e:
        print(f"❌ log_search error: {e}")


# 🧪 Test DB
async def test_db_connection():
    db = get_db()
    try:
        async with db.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM users LIMIT 5;")

        print("✅ DB Connected:", [dict(r) for r in rows])
        return rows

    except Exception as e:
        print(f"❌ test_db_connection error: {e}")
        return []