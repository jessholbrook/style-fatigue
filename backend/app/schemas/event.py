from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EventIn(BaseModel):
    event_type: str
    payload: dict = {}
    session_id: UUID | None = None
    client_timestamp: datetime | None = None
