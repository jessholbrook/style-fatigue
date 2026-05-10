from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ParticipantCreate(BaseModel):
    metadata_json: dict | None = None


class ParticipantResponse(BaseModel):
    id: UUID
    token: str
    condition: str | None
    created_at: datetime
    consent_given_at: datetime | None
    is_active: bool
    session_count: int = 0

    model_config = {"from_attributes": True}


class ConsentRequest(BaseModel):
    agreed: bool
