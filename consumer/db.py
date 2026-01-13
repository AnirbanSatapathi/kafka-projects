import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
)

conn.autocommit = False

def insert_events(events: list[dict]):
    query = """
        INSERT INTO events (
            event_id, user_id, event_type, page, event_time, received_at
        ) VALUES %s
        ON CONFLICT (event_id) DO NOTHING
    """
    
    values = [
        (
            e["event_id"],
            e["user_id"],
            e["event_type"],
            e["page"],
            e["event_time"],
            e["received_at"],
        )
        for e in events
    ]

    with conn.cursor() as cur:
        execute_values(cur, query, values)