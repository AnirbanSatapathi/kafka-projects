from confluent_kafka import Consumer
import json,signal,sys,time

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

consumer = Consumer(conf)
consumer.subscribe(["raw_events"])

def shutdown(sig, frame):
    print("Shutting down consumer...")
    consumer.close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

print("Consumer started...")

BATCH_SIZE = 100
POLL_TIMEOUT = 1.0
FLUSH_INTERVAL = 2.0 

batch = []
last_flush_time = time.time()

try:
    while True:
        msg = consumer.poll(POLL_TIMEOUT)
        if msg is None:
            pass
        elif msg.error():
            print(f"Consumer error: {msg.error()}")
        else:
            raw_val = msg.value()
            if raw_val is None or len(raw_val) == 0:
                print("Warning: Received empty message")
            else:
                try:
                    val_str = raw_val.decode("utf-8")
                    event = json.loads(val_str)
                    batch.append(event)
                except json.JSONDecodeError:
                    print(f"Failed to decode: {raw_val}")
                except Exception as e:
                    print(f"ERROR: Unexpected error: {e}")
        now = time.time()
        should_flush = (
            len(batch) >= BATCH_SIZE or
            (batch and now - last_flush_time >= FLUSH_INTERVAL)
        )
        if should_flush:
            print(f"Processing batch of size {len(batch)}...")
            for e in batch:
                pass 
            consumer.commit(asynchronous=False)
            print("Commit successful.")
            batch.clear()
            last_flush_time = now

except KeyboardInterrupt:
    pass
finally:
    consumer.close()