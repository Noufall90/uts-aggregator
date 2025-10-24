from pydantic import BaseModel
from typing import Dict, Any, List, Union

class Event(BaseModel):
    topic: str
    event_id: str
    timestamp: str  # ISO8601
    source: str
    payload: Dict[str, Any]

class PublishRequest(BaseModel):
    events: Union[Event, List[Event]]
