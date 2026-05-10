from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SessionResponse(BaseModel):
    id: UUID
    session_number: int
    style_profile: str
    started_at: datetime
    completed_at: datetime | None
    is_shift_session: bool

    model_config = {"from_attributes": True}
