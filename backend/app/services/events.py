from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.event_log import EventLog


def log_event(
    db: Session,
    participant_id: UUID | None,
    session_id: UUID | None,
    event_type: str,
    payload: dict | None = None,
    client_timestamp: datetime | None = None,
) -> None:
    """Stage an event row. The caller owns the commit."""
    db.add(
        EventLog(
            participant_id=participant_id,
            session_id=session_id,
            event_type=event_type,
            payload=payload or {},
            client_timestamp=client_timestamp,
        )
    )
