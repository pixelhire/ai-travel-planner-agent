from backend.messaging.base_worker import start_worker

def hotels_query(data):
    return f"""
You are a travel expert.

Suggest REAL hotels.

Destination: {data['destination']}
Budget: {data['budget']}

Rules:
- ONLY use the given destination
- Include:
  - budget hotels
  - mid-range hotels
  - luxury hotels
- Mention approximate price per night

Return clean structured list.
"""

start_worker("hotels_topic", "hotels_workers", "hotels", hotels_query)