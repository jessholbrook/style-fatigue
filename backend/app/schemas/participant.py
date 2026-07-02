from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ParticipantCreate(BaseModel):
    metadata_json: dict | None = None


# Participant-facing: deliberately excludes condition/shift_eligible_at —
# participants must not be able to unblind themselves via the network tab.
class ParticipantResponse(BaseModel):
    id: UUID
    token: str
    created_at: datetime
    consent_given_at: datetime | None
    is_active: bool
    completed_sessions: int = 0

    model_config = {"from_attributes": True}


class ConsentRequest(BaseModel):
    agreed: bool
