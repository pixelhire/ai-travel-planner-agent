from langchain.agents import initialize_agent
from langchain.tools import Tool

from backend.tools.destination_tool import search_destination
from backend.tools.itinerary_tool import generate_itinerary
from backend.tools.activity_tools import find_activities
from backend.tools.hotel_tool import find_hotels
from backend.tools.transport_tool import find_transport
from backend.tools.weater_tool import find_weather

from backend.utils.llm import get_llm


llm = get_llm()

tools = [

    Tool(
        name="Destination Research",
        func=search_destination,
        description="Search tourist attractions for a destination"
    ),

    Tool(
        name="Find Activities",
        func=find_activities,
        description="Find activities and things to do at destination"
    ),

    Tool(
        name="Find Hotels",
        func=find_hotels,
        description="Find hotels or accommodations at destination"
    ),

    Tool(
        name="Find Weather",
        func=find_weather,
        description="Get weather and best season for destination"
    ),

    Tool(
        name="Find Transport",
        func=find_transport,
        description="Find transport options for destination"
    ),

    # Tool(
    #     name="Generate Itinerary",
    #     func=generate_itinerary,
    #     description="Generate day-wise travel itinerary"
    # ),
]


travel_agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True,
)


#this is commented because not using langchane now .. Using only kafka 
# def run_travel_agent(query: str):
#     response = travel_agent.run(query)
#     return response



def run_travel_agent(query: str):
    response = llm.invoke(query)

    try:
        return response.content.strip()
    except:
        return ""