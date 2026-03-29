import sys
import os
import json
from kafka import KafkaConsumer

# ✅ Fix import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.agents.travel_agent import run_travel_agent
from backend.memory.trip_store import save_result


def build_query(task, destination, budget, days):
    if task == "activities":
        return f"Top activities in {destination} for {days} days"
    elif task == "hotels":
        return f"Best {budget} hotels in {destination}"
    elif task == "itinerary":
        return f"{days}-day itinerary for {destination}"
    elif task == "budget":
        return f"Budget breakdown for {destination}"
    elif task == "transport":
        return f"Transport options in {destination}"
    elif task == "weather":
        return f"Weather updates in {destination}"
    return f"Travel plan for {destination}"


if __name__ == "__main__":

    consumer = KafkaConsumer(
        "activities_topic",
        "hotels_topic",
        "itinerary_topic",
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
            task = message.topic.replace("_topic", "")  # 🔥 key trick
            data = message.value

            print(f"📥 Received {task} task")

            destination = data["destination"]
            trip_id = data["trip_id"]
            budget = data.get("budget", "medium")
            days = data.get("days", 3)

            query = build_query(task, destination, budget, days)

            result = run_travel_agent(query)

            save_result(trip_id, task, result)

            print(f"✅ {task} saved for {destination}")

        except Exception as e:
            print(f"❌ Worker error:", e)