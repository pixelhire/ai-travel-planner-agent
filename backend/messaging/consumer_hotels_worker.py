# from backend.messaging.base_worker import start_worker

def hotels_query(data):
    return f"""
You are a travel expert.

Suggest REAL hotels.

Destination: {data['destination']}
Budget: {data['budget']}

RULES:
- ONLY use the given destination
- Provide real hotel names
- Include price per night
- Include budget, mid-range, and luxury options
- NEVER return "Not available"

OUTPUT FORMAT (STRICT JSON):

{{
  "hotels": [
    {{
      "name": "",
      "price_per_night": "",
      "category": "budget/mid/luxury"
    }}
  ]
}}
"""

# start_worker("hotels_topic", "hotels_workers", "hotels", hotels_query)