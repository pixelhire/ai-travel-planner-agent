import json
import time
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

TOPICS = {
    "activities": "activities_topic",
    "hotels": "hotels_topic",
    "transport": "transport_topic",
    "weather": "weather_topic",
    "itinerary": "itinerary_topic",
    "budget": "budget_topic",
}

# 🔥 Create producer with retry
def create_producer(retries=5, delay=2):
    for attempt in range(retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers="localhost:9092",
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            print("✅ Kafka Producer connected")
            return producer

        except NoBrokersAvailable:
            print(f"⏳ Kafka not available (attempt {attempt + 1}/{retries})...")
            time.sleep(delay)

    raise Exception("❌ Failed to connect to Kafka after retries")


# Lazy init (important)
producer = None

def get_producer():
    global producer
    if producer is None:
        producer = create_producer()
    return producer


# 🔥 Send task safely
def send_task(task_type, data):
    print("Task :",task_type)
    print("Data :",data)
    topic = TOPICS.get(task_type)

    if not topic:
        raise ValueError(f"Invalid task type: {task_type}")

    try:
        kafka_producer = get_producer()
        kafka_producer.send(topic, data)

        print(f"📤 Sent task → {topic}: {data}")

    except Exception as e:
        print(f"❌ Failed to send task: {e}")