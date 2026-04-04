#!/bin/bash

echo "Creating Kafka topics..."

topics=(
  activities_topic
  hotels_topic
  # itinerary_topic
  budget_topic
  transport_topic
  weather_topic
)

for topic in "${topics[@]}"
do
  kafka-topics --create \
    --topic "$topic" \
    --bootstrap-server localhost:9092 \
    --partitions 3 \
    --replication-factor 1 \
    --if-not-exists
done

echo "✅ Kafka topics created"


# run the script : bash scripts/create_topics.sh

# run below command to see the kafka details :

# kafka-topics \
# --describe \
# --topic research_topic \
# --bootstrap-server localhost:9092