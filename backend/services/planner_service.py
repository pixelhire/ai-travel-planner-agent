# from backend.agents.travel_agent import travel_agent
import json
import re
from backend.utils.llm import get_llm
from backend.agents.travel_agent import run_travel_agent

llm = get_llm()


# 🔥 Extract destination (fast + reliable)
import re

import re

STOP_WORDS = {
    "trip", "plan", "days", "day", "travel",
    "itinerary", "visit", "places", "for", "to", "in"
}

def extract_destination(query: str) -> str:
    query = query.lower()

    # 🔥 1. try "to <place>" or "for <place>" or "in <place>"
    match = re.search(r"(?:to|for|in)\s+([a-zA-Z\s]+?)(?:\s+\d+|\s+day|\s+days|$)", query)
    if match:
        dest = match.group(1).strip()

        # clean trailing words
        dest = re.sub(r"\b(for|with|under|of|during|in)\b.*", "", dest)

        if dest and dest not in STOP_WORDS:
            return dest.title()

    # 🔥 2. fallback: pick meaningful word (not stopword)
    words = query.split()

    for word in words:
        if word.isalpha() and word not in STOP_WORDS:
            return word.title()

    return "Unknown"




# 🔥 Extract days (optional but useful)
def extract_days(query: str) -> int | None:
    match = re.search(r"(\d+)\s*day", query.lower())
    if match:
        return int(match.group(1))
    return None


def plan_trip(query: str):

    # ✅ deterministic extraction first
    destination = extract_destination(query)
    days = extract_days(query)

    if not days:
        match = re.search(r"(\d+)", query)
        if match:
            days = int(match.group(1))

    if not days:
        days = 3

    prompt = f"""
You are a travel planner AI.

Analyze the query and decide ONLY the relevant planning tasks.

Query: {query}

Rules:
- Do NOT include "destination" as a task
- Only include necessary tasks
- Keep tasks from this list only:
  ["activities", "hotels", "transport", "weather", "budget"]

Return ONLY valid JSON. No explanation.

Format:
{{
  "tasks": [...]
}}
"""

    response = llm.invoke(prompt)
    content = response.content.strip()

    tasks = []

    try:
        parsed = json.loads(content)
        tasks = parsed.get("tasks", [])
    except:
        # 🔥 safer extraction
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
                tasks = parsed.get("tasks", [])
            except:
                pass

    # 🔥 fallback if LLM fails
    if not tasks:
        tasks = ["activities", "hotels", "transport", "weather", "budget"]

    # 🔥 sanitize tasks (IMPORTANT)
    allowed = {"activities", "hotels", "transport", "weather",  "budget"}
    tasks = [t for t in tasks if t in allowed]

    # ensure minimum tasks
    if "activities" not in tasks:
        tasks.append("activities")

    return {
        "destination": destination,
        "days": days,
        "tasks": tasks
    }


# def build_final_response(trip_data):

#     prompt = f"""
#     You are a travel planner.

#     Convert this raw data into structured JSON:

#     {trip_data}

#     Output format:
#     {{
#         "summary": "...",
#         "activities": [...],
#         "hotels": [...],
#         "itinerary": [...]
#     }}
#     """

#     return llm.invoke(prompt)


def generate_final_plan(results, destination, days, transport=None, weather=None):
    # =========================================================
    # ✅ SAFE FALLBACKS
    # =========================================================
    days = int(days) if days else 3

    hotels = results.get("hotels") or "Not available"
    activities = results.get("activities") or "Not available"
    budget = results.get("budget") or "Not available"

    # prefer explicit args if passed, else fallback to results
    transport_data = transport or results.get("transport") or "Not available"
    weather_data = weather or results.get("weather") or "Not available"
    itinerary_input = results.get("itinerary") or ""

    # =========================================================
    # 🔥 STRICT PROMPT (ANTI-HALLUCINATION)
    # =========================================================
    prompt = f"""
You are a professional travel planner.

Create a STRICT {days}-day travel plan for {destination}.

IMPORTANT RULES:
- The itinerary MUST be exactly {days} days (no more, no less)
- Do NOT add extra days
- Do NOT assume default durations like 3 or 5 days
- Use ONLY the provided data
- DO NOT use markdown (*, #, -, etc.)
- If some data is missing, still keep the plan realistic

---------------------
DATA PROVIDED:

Activities:
{activities}

Hotels:
{hotels}

Transport:
{transport_data}

Weather:
{weather_data}

Budget:
{budget}

Raw Itinerary Input:
{itinerary_input}

---------------------

OUTPUT FORMAT:

Start EXACTLY like this:

Here is a detailed {days}-day travel itinerary for {destination}:

Best Season to Visit:
- Provide based on weather data

Transportation:
- Provide transport options with cost

Accommodation:
- List recommended hotels

Itinerary:

Day 1: <Title>
- Activity 1
- Activity 2
- Activity 3

Day 2:
...

(continue until Day {days})

Estimated Budget:
- Transport: 
- Hotels: 
- Food: 
- Activities: 
- Total: 

Final line:
This itinerary provides a balanced mix of travel, exploration, and experience.
"""

    # =========================================================
    # ✅ CALL AGENT
    # =========================================================
    # response = run_travel_agent(prompt)

    # =========================================================
    # ✅ SAFETY CLEANUP (important for UI)
    # =========================================================

    response = llm.invoke(prompt)

    if isinstance(response, str):
        return response.strip()

    return str(response)
    