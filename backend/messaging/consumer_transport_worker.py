from backend.messaging.base_worker import start_worker

def transport_query(data):
    return f"""
You are a travel expert.

Provide transport details.

Destination: {data['destination']}

Include:
- how to reach (flight/train)
- local transport
- cost estimates

ONLY use the given destination.
"""

start_worker("transport_topic", "transport_workers", "transport", transport_query)