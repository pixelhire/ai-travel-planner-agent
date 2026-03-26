from backend.utils.llm import get_llm
import json


llm = get_llm()


def generate_itinerary(query :str):


    prompt = f"""
You are an expert travel planner.

Create a detailed travel itinerary.

User request:
{query}

Return ONLY valid JSON.

Do NOT include explanations, markdown, or text outside JSON.

Use this exact schema:

{{
  "destination": "",
  "days": 0,
  "best_season": "",
  "weather": "",
  "transport": "",
  "accommodation": "",
  "itinerary": [
    {{
      "day": 1,
      "title": "",
      "activities": []
    }}
  ],
  "budget": {{
    "transport": 0,
    "hotels": 0,
    "food": 0,
    "activities": 0,
    "total": 0
  }}
}}
"""
    
    # print("making plan for :\n",prompt)
    response = llm.invoke(prompt)
    result = response.content
    return result