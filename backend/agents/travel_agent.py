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
        description="Search tourist attraction for the destination"
    ),
    Tool(
        name="Generate Itinerary",
        func=generate_itinerary,
        description="Generate day wise travel itinerary"
    ),
    Tool(
        name="Find Hotest or Accomodations",
        func=find_hotels,
        description="Find hotels for the destination"
    ),
    Tool(
        name="Find Activities",
        func=find_activities,
        description="Find activities to do in destination"
    ),
    Tool(
        name="Find Weather",
        func=find_weather,
        description="Find weather updates for the destination"
    ),
    Tool(
        name="Find Transport",
        func=find_transport,
        description="Find transport detials for the dstination"
    ),
    

]

travel_agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
)