import os,sys,json,signal,time
from datetime import datetime, timezone
from confluent_kafka import Consumer
from dotenv import load_dotenv, find_dotenv
from db import insert_events, conn

load_dotenv(find_dotenv())

KAFKA_CONF = {
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    "security.protocol": "SASL_PLAINTEXT",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": os.getenv("KAFKA_SASL_USER"),
    "sasl.password": os.getenv("KAFKA_SASL_PASS"),
    "group.id": os.getenv("KAFKA_GROUP_ID"),
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
}

consumer = Consumer(KAFKA_CONF)
consumer.subscribe([os.getenv("KAFKA_TOPIC")])

def shutdown(sig, frame):
    print("Shutting down consumer...")
    consumer.close()
    conn.close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

print("Consumer started... Waiting for batch...")

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
            if msg.value():
                try:
                    event = json.loads(msg.value().decode("utf-8"))
                    batch.append(event)
                except Exception as e:
                    print(f"Decode error: {e}")

        # Flush Logic
        now = time.time()
        should_flush = (len(batch) >= BATCH_SIZE or 
                       (batch and now - last_flush_time >= FLUSH_INTERVAL))

        if should_flush:
            print(f"Processing batch of size {len(batch)}...")
            try:
                for e in batch:
                    e["received_at"] = datetime.now(timezone.utc)
                
                insert_events(batch)
                conn.commit()
                consumer.commit(asynchronous=False)
                print("Batch committed.")
            except Exception as e:
                print(f"CRITICAL DB ERROR: {e}")
                conn.rollback()
            
            batch.clear()
            last_flush_time = now

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
    conn.close()