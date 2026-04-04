# from backend.messaging.base_worker import start_worker

def transport_query(data):
    return f"""
You are a travel expert.

Provide transport details.

Destination: {data['destination']}

RULES:
- ONLY use the given destination
- Include realistic transport options
- Include cost estimates
- NEVER return "Not available"

OUTPUT FORMAT (STRICT JSON):

{{
  "transport": [
    {{
      "type": "flight/train/local",
      "details": "",
      "estimated_cost": ""
    }}
  ]
}}
"""

# start_worker("transport_topic", "transport_workers", "transport", transport_query)