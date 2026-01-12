from fastapi import FastAPI, status
from schemas import EventIn

app = FastAPI(title="Clickstream Ingestion API")

@app.post("/events", status_code=status.HTTP_202_ACCEPTED)
async def ingest_event(event: EventIn):
    # Kafka will come later
    return {"status": "queued"}