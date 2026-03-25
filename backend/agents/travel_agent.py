from langchain.agents import initialize_agent
from langchain.tools import Tool
from backend.tools.destination_tool import search_destination
from backend.tools.itinerary_tool import generate_itinerary
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

]

travel_agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
)