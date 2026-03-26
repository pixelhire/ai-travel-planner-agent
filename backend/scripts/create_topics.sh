#!/bin/bash

echo "Creating Kafka topics..."

kafka-topics --create \
--topic research_topic \
--bootstrap-server localhost:9092 \
--partitions 5 \
--replication-factor 1

kafka-topics --create \
--topic hotel_topic \
--bootstrap-server localhost:9092 \
--partitions 3 \
--replication-factor 1

kafka-topics --create \
--topic transport_topic \
--bootstrap-server localhost:9092 \
--partitions 3 \
--replication-factor 1

echo "Kafka topics created"


# run the script : bash scripts/create_topics.sh

# run below command to see the kafka details :

# kafka-topics \
# --describe \
# --topic research_topic \
# --bootstrap-server localhost:9092