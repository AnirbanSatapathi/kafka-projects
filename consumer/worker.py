from confluent_kafka import Consumer
import json, signal, sys

conf = {
    "bootstrap.servers": "192.168.20.17:3420",
    "security.protocol": "SASL_PLAINTEXT",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": "admin",
    "sasl.password": "Nrxen@2026",
    "group.id": "event_ingestors",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
}

Consumer = Consumer(conf)
Consumer.subscribe(["raw_events"])

def shutdown(sig, frame):
    print("Shutting down consumer...")
    Consumer.close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

print("Consumer started... Waiting for messages")

try:
    while True:
        msg = Consumer.poll(1.0)
        if msg is None:
            continue

        raw_val = msg.value()
        if raw_val is None or len(raw_val)==0:
            print("Warning: Received empty message")
            continue

        try:
            val_str = raw_val.decode("utf-8")
            event = json.loads(val_str)
            print("consumed: ", event)
        except json.JSONDecodeError as e :
            print(f"Failed to decode: {raw_val}")
        except Exception as e:
            print(f"ERROR: Unexpected error: {e}")
            continue
except KeyboardInterrupt:
    pass
finally:
    Consumer.close()