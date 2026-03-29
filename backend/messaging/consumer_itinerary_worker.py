from backend.messaging.base_worker import start_worker

def itinerary_query(data):
    return f"""
You are a travel planner.

Create a detailed itinerary.

Destination: {data['destination']}
Duration: {data['days']} days
Budget: {data['budget']}

Rules:
- ONLY use the given destination
- DO NOT switch cities
- Provide day-wise breakdown
- Include places + activities

Return structured day-by-day plan.
"""

start_worker("itinerary_topic", "itinerary_workers", "itinerary", itinerary_query)