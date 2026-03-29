from backend.messaging.base_worker import start_worker

def budget_query(data):
    return f"""
You are a travel planner.

Create a realistic budget.

Destination: {data['destination']}
Duration: {data['days']} days
Budget type: {data['budget']}

Include:
- hotel cost
- food cost
- transport cost
- activities cost
- total estimate

Return clean breakdown.
"""

start_worker("budget_topic", "budget_workers", "budget", budget_query)