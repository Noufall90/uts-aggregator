from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
import asyncio
import logging
import time
from typing import List, Dict, Any
from models import Event, PublishRequest
from database import init_db, is_processed, mark_processed, get_events_by_topic

app = FastAPI()
queue = asyncio.Queue()
logger = logging.getLogger(__name__)

stats = {
    "received": 0,
    "unique_processed": 0,
    "duplicate_dropped": 0,
    "topics": set(),
    "uptime_start": time.time()
}

async def consumer():
    await init_db()
    while True:
        event = await queue.get()
        if await is_processed(event.topic, event.event_id):
            stats["duplicate_dropped"] += 1
            logger.info(f"Duplicate: {event.topic}/{event.event_id}")
        else:
            await mark_processed(event)
            stats["unique_processed"] += 1
            stats["topics"].add(event.topic)
            logger.info(f"Processed: {event.topic}/{event.event_id}")
        queue.task_done()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consumer())

@app.post("/publish")
async def publish_events(request: PublishRequest):
    events = request.events if isinstance(request.events, list) else [request.events]
    for event in events:
        try:
            Event(**event.dict())
            await queue.put(event)
            stats["received"] += 1
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {"status": "accepted", "count": len(events)}

@app.get("/events")
async def get_events(topic: str) -> List[Dict[str, Any]]:
    return await get_events_by_topic(topic)

@app.get("/stats")
async def get_stats():
    return {
        "received": stats["received"],
        "unique_processed": stats["unique_processed"],
        "duplicate_dropped": stats["duplicate_dropped"],
        "topics": list(stats["topics"]),
        "uptime": time.time() - stats["uptime_start"],
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}
