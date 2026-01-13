from fastapi import FastAPI, status
from schemas import EventIn
from producer import produce_event

app = FastAPI(title="Clickstream Ingestion API")

@app.post("/events", status_code=status.HTTP_202_ACCEPTED)
async def ingest_event(event: EventIn):
    produce_event(event.model_dump(mode='json'))
    return {"status": "queued"}