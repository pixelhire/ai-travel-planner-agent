# from backend.messaging.base_worker import start_worker

def weather_query(data):
    return f"""
You are a travel assistant.

Provide weather details.

Destination: {data['destination']}

RULES:
- ONLY use the given destination
- Provide realistic seasonal info

OUTPUT FORMAT (STRICT JSON):

{{
  "current_weather": "",
  "best_time_to_visit": "",
  "travel_tip": ""
}}
"""

# start_worker("weather_topic", "weather_workers", "weather", weather_query)