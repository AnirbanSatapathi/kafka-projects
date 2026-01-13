import os
import json
from confluent_kafka import Producer
from dotenv import load_dotenv, find_dotenv

# Find and load the .env file automatically (even if inside subfolders)
load_dotenv(find_dotenv())

# Fetch from Environment
BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
SASL_USER = os.getenv("KAFKA_SASL_USER")
SASL_PASS = os.getenv("KAFKA_SASL_PASS")
TOPIC = os.getenv("KAFKA_TOPIC")

if not BOOTSTRAP_SERVERS:
    raise ValueError("Missing .env configuration for Kafka")

KAFKA_CONF = {
    "bootstrap.servers": BOOTSTRAP_SERVERS,
    "security.protocol": "SASL_PLAINTEXT",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": SASL_USER,
    "sasl.password": SASL_PASS,
    "linger.ms": 10,
}

producer = Producer(KAFKA_CONF)

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else: print(f"Sent to {msg.topic()}") # Optional: Quiet mode

def produce_event(event: dict):
    producer.produce(
        topic=TOPIC,
        key=str(event["user_id"]),
        value=json.dumps(event),
        on_delivery=delivery_report,
    )
    producer.poll(0)