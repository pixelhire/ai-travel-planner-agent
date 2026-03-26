from backend.utils.llm import get_llm
import json


llm = get_llm()


def generate_itinerary(query :str):


    prompt = f""" 
You are an expert travel planner.

Create a detailed travel plan. 

User Request:
{query}

Include :
- best attractions
- recommended hotels
- transport suggestions
- food experience
- daily activities
- estinamte budget

Return ONLY VALID JSON.

Do NOT return explanation text.
Do NOT return markdown.
Do NOT return bullet points.


Return ONLY valid JSON in this format:

{{
  "destination": "",
  "days": 0,
  "best_season": "",
  "weather": "",
  "transport":"",
  "accommodation":"",
  "itinerary": [
    {{
      "day": 1,
      "activities": []
    }}
  ],
  "budget": {{
    "transport": 0,
    "hotels": 0,
    "food": 0,
    "activities": 0,
    "total":0
  }}
}}
"""
    
    # print("making plan for :\n",prompt)
    response = llm.invoke(prompt)
    result = response.content
    return result