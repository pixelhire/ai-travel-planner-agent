from backend.agents.travel_agent import travel_agent

def plan_trip(query: str):
    result = travel_agent.invoke(query)
    return result