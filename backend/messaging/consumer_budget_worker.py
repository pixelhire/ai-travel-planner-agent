# from backend.messaging.base_worker import start_worker

def budget_query(data):
    return f"""
You are a travel planner.

Create a realistic budget.

Destination: {data['destination']}
Duration: {data['days']} days
Budget type: {data['budget']}

RULES:
- Provide realistic cost estimates
- NEVER return "Not available"
- Use approximate ranges if unsure

OUTPUT FORMAT (STRICT JSON):

{{
  "stay_per_night": "",
  "food_per_day": "",
  "transport": "",
  "activities": "",
  "total_estimate": ""
}}
"""

# start_worker("budget_topic", "budget_workers", "budget", budget_query)