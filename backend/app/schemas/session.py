from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.conversation import ConversationResponse


# Participant-facing: deliberately excludes style_profile/is_shift_session.
class SessionResponse(BaseModel):
    id: UUID
    session_number: int
    started_at: datetime
    completed_at: datetime | None

    model_config = {"from_attributes": True}


class SessionStartResponse(BaseModel):
    session: SessionResponse
    conversation: ConversationResponse | None = None
    resumed: bool = False
