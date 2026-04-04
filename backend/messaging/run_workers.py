import sys
import os
import json
from kafka import KafkaConsumer

# ✅ Fix import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.agents.travel_agent import run_travel_agent
from backend.memory.trip_store import save_result

# ✅ Import task-specific prompt builders
from backend.messaging.consumer_activities_worker import activities_query
from backend.messaging.consumer_hotels_worker import hotels_query
from backend.messaging.consumer_transport_worker import transport_query
from backend.messaging.consumer_weather_worker import weather_query
from backend.messaging.consumer_budget_worker import budget_query


# ✅ Map task → prompt function
TASK_QUERY_MAP = {
    "activities": activities_query,
    "hotels": hotels_query,
    "transport": transport_query,
    "weather": weather_query,
    "budget": budget_query,
}


if __name__ == "__main__":

    consumer = KafkaConsumer(
        "activities_topic",
        "hotels_topic",
        # "itinerary_topic",
        "budget_topic",
        "transport_topic",
        "weather_topic",
        bootstrap_servers="localhost:9092",
        group_id="trip_workers",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )

    print("🚀 Single worker started for all topics...")

    for message in consumer:
        try:
            task = message.topic.replace("_topic", "")
            data = message.value

            print(f"\n📥 Received task: {task}")

            destination = data["destination"]
            trip_id = data["trip_id"]
            budget = data.get("budget", "medium")
            days = data.get("days", 3)

            # ✅ Build input data for prompt
            input_data = {
                "destination": destination,
                "budget": budget,
                "days": days,
                "query": data.get("query", "")
            }

            # ✅ Get correct query function
            query_fn = TASK_QUERY_MAP.get(task)

            if not query_fn:
                raise ValueError(f"❌ No query function found for task: {task}")

            query = query_fn(input_data)

            # 🔥 Debug logs (VERY IMPORTANT)
            print(f"🔥 TASK: {task}")
            # print(f"📍 DESTINATION: {destination}")
            # print(f"📜 PROMPT:\n{query}\n")

            # ✅ Call LLM (no agent now)
            result = run_travel_agent(query)

            # 🔥 Debug result
            # print(f"📦 RESULT (raw): {result}")

            # ✅ Save result
            save_result(trip_id, task, result)

            print(f"✅ {task} saved for {destination}")

        except Exception as e:
            print(f"❌ Worker error in task [{task}]:", e)