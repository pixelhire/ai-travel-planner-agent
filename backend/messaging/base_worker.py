from kafka import KafkaConsumer
import json
from backend.agents.travel_agent import run_travel_agent
from backend.memory.trip_store import save_result


def start_worker(topic, group_id, task_key, build_query):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers="localhost:9092",
        group_id=group_id,
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )

    print(f"🚀 {task_key.capitalize()} worker started...")

    for message in consumer:
        try:
            task = message.value

            trip_id = task["trip_id"]

            # 🔥 FULL CONTEXT (IMPORTANT)
            data = {
                "destination": task.get("destination"),
                "budget": task.get("budget", "medium"),
                "days": task.get("days", 3),
                "query": task.get("query", "")
            }

            # 🔥 build strong prompt
            query = build_query(data)

            print(f"\n📍 TASK: {task_key}")
            print(f"📍 DESTINATION: {data['destination']}")
            print(f"📍 QUERY: {data['query']}")
            print(f"📍 FINAL PROMPT:\n{query}\n")

            result = run_travel_agent(query)

            save_result(trip_id, task_key, result)

            print(f"✅ {task_key} saved for {data['destination']}")

        except Exception as e:
            print(f"❌ {task_key} worker error:", e)