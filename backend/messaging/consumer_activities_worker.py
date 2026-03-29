from backend.messaging.base_worker import start_worker

def activities_query(data):
    return f"""
You are a travel expert.

Generate REAL and SPECIFIC activities.

Destination: {data['destination']}
Duration: {data['days']} days
Budget: {data['budget']}

Rules:
- ONLY use the given destination
- DO NOT mention any other city
- Include real attractions and experiences
- Add approximate cost per activity

Return clean bullet points.
"""

start_worker("activities_topic", "activities_workers", "activities", activities_query)