# from backend.messaging.base_worker import start_worker

def activities_query(data):
    return f"""
You are a travel expert.

Generate REAL and SPECIFIC activities.

Destination: {data['destination']}
Duration: {data['days']} days
Budget: {data['budget']}

RULES:
- ONLY use the given destination
- DO NOT mention any other city
- Use real attraction names
- Avoid generic phrases like "local market"
- Each activity MUST include estimated cost
- NEVER return "Not available"

OUTPUT FORMAT (STRICT JSON):

{{
  "activities": [
    {{
      "name": "",
      "location": "",
      "estimated_cost": ""
    }}
  ]
}}
"""

# start_worker("activities_topic", "activities_workers", "activities", activities_query)