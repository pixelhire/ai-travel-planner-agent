from backend.messaging.base_worker import start_worker

def weather_query(data):
    return f"""
You are a travel assistant.

Provide weather details.

Destination: {data['destination']}

Include:
- current weather
- best time to visit
- travel tips

ONLY use the given destination.
"""

start_worker("weather_topic", "weather_workers", "weather", weather_query)