from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ConversationStart(BaseModel):
    intent: str
    topic: str


class MessageIn(BaseModel):
    content: str


class MessageOut(BaseModel):
    role: str
    content: str
    timestamp: datetime


class ConversationResponse(BaseModel):
    id: UUID
    intent: str
    topic: str
    messages: list[MessageOut]
    turn_count: int
    started_at: datetime
    completed_at: datetime | None

    model_config = {"from_attributes": True}
