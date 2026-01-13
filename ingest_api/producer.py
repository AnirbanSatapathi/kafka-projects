from confluent_kafka import Producer
import json

KAFKA_CONF ={
    "bootstrap.servers": "192.168.20.17:3420",
    "security.protocol": "SASL_PLAINTEXT",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": "admin",
    "sasl.password": "Nrxen@2026",
    "linger.ms": 10,  # Wait 10ms to batch messages
}

producer = Producer(KAFKA_CONF)

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def produce_event(event: dict):
    producer.produce(
        topic="raw_events",
        key=str(event["user_id"]),
        value=json.dumps(event),
        on_delivery=delivery_report,
    )
    # Poll triggers the delivery report
    producer.poll(0)
