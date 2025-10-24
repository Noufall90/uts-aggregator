from typing import Any, Dict, List
import aiosqlite
import asyncio
import os
import json

DB_PATH = "/app/data/dedup.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS processed_events (
                topic TEXT,
                event_id TEXT,
                timestamp TEXT,
                source TEXT,
                payload TEXT,
                PRIMARY KEY (topic, event_id)
            )
        """)
        await db.commit()

async def is_processed(topic: str, event_id: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT 1 FROM processed_events WHERE topic = ? AND event_id = ?",
            (topic, event_id)
        )
        result = await cursor.fetchone()
        return result is not None

async def mark_processed(event):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO processed_events (topic, event_id, timestamp, source, payload) VALUES (?, ?, ?, ?, ?)",
            (event.topic, event.event_id, event.timestamp, event.source, json.dumps(event.payload))
        )
        await db.commit()

async def get_events_by_topic(topic: str) -> List[Dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT topic, event_id, timestamp, source, payload FROM processed_events WHERE topic = ?",
            (topic,)
        )
        rows = await cursor.fetchall()
        return [
            {
                "topic": row[0],
                "event_id": row[1],
                "timestamp": row[2],
                "source": row[3],
                "payload": json.loads(row[4]),
            }
            for row in rows
        ]
