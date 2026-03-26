from kafka import KafkaConsumer
import json

from backend.agents.travel_agent import run_travel_agent

consumer = KafkaConsumer(
    "research_topic",
    bootstrap_servers="localhost:9092",
    group_id="research_workers",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

for message in consumer:

    try:

        task = message.value
        destination = task["destination"]

        query = f"Find attractions and activities in {destination}"

        result = run_travel_agent(query)

        print("Research result:\n", result)

    except Exception as e:

        print("Worker error:", e)