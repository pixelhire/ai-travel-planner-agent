from backend.utils.llm import get_llm
import json


llm = get_llm()


def generate_itinerary(query :str):


    prompt = f""" 
Create a travel plan for the following request:

{query}

Return ONLY valid JSON in this format:

{{
  "destination": "",
  "days": 0,
  "total_budget": 0,
  "best_season": "",
  "weather": "",
  "itinerary": [
    {{
      "day": 1,
      "activities": []
    }}
  ],
  "budget": {{
    "flights": 0,
    "hotels": 0,
    "food": 0,
    "activities": 0
  }}
}}
"""
    
    # print("making plan for :\n",prompt)
    response = llm.invoke(prompt)
    result = response.content
    return result