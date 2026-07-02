from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.conversation import Conversation
from app.models.session import ExperimentSession
from app.routers.participants import completed_session_count, get_participant_by_token
from app.schemas.session import SessionResponse, SessionStartResponse
from app.services import experiment as experiment_service

router = APIRouter(tags=["sessions"])


def as_utc(dt: datetime | None) -> datetime | None:
    """SQLite returns naive datetimes; Postgres returns aware. Normalize."""
    if dt is not None and dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def get_owned_session(token: str, session_id: UUID, db: Session) -> ExperimentSession:
    participant = get_participant_by_token(token, db)
    session = (
        db.query(ExperimentSession)
        .filter(
            ExperimentSession.id == session_id,
            ExperimentSession.participant_id == participant.id,
        )
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/participants/{token}/sessions", response_model=SessionStartResponse)
def start_session(token: str, db: Session = Depends(get_db)):
    participant = get_participant_by_token(token, db)
    if not participant.consent_given_at:
        raise HTTPException(status_code=400, detail="Consent required before starting sessions")

    config = experiment_service.load_experiment_config()
    now = datetime.now(timezone.utc)

    # Resume an open session instead of rejecting — covers refresh-mid-chat
    # and React StrictMode's double effect in dev.
    latest = (
        db.query(ExperimentSession)
        .filter(ExperimentSession.participant_id == participant.id)
        .order_by(ExperimentSession.session_number.desc())
        .first()
    )
    if latest and not latest.completed_at:
        conversation = (
            db.query(Conversation).filter(Conversation.session_id == latest.id).first()
        )
        return SessionStartResponse(
            session=SessionResponse.model_validate(latest),
            conversation=conversation,
            resumed=True,
        )

    completed = completed_session_count(participant, db)
    if completed >= config.get("max_sessions", 6):
        raise HTTPException(status_code=409, detail={"reason": "study_complete"})

    study_start = as_utc(participant.consent_given_at or participant.created_at)
    expiry_days = config.get("session_expiry_days", 14)
    if study_start and now > study_start + timedelta(days=expiry_days):
        raise HTTPException(status_code=410, detail={"reason": "study_expired"})

    cooldown_hours = config.get("session_cooldown_hours", 48)
    if latest and latest.completed_at:
        next_available = as_utc(latest.completed_at) + timedelta(hours=cooldown_hours)
        if now < next_available:
            raise HTTPException(
                status_code=409,
                detail={
                    "reason": "cooldown",
                    "next_available_at": next_available.isoformat(),
                },
            )

    next_number = (latest.session_number + 1) if latest else 1
    is_shift, style_profile = experiment_service.determine_style_profile(
        participant, next_number, db
    )

    session = ExperimentSession(
        participant_id=participant.id,
        session_number=next_number,
        style_profile=style_profile,
        is_shift_session=is_shift,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return SessionStartResponse(session=SessionResponse.model_validate(session))


@router.get("/participants/{token}/sessions", response_model=list[SessionResponse])
def list_sessions(token: str, db: Session = Depends(get_db)):
    participant = get_participant_by_token(token, db)
    return (
        db.query(ExperimentSession)
        .filter(ExperimentSession.participant_id == participant.id)
        .order_by(ExperimentSession.session_number)
        .all()
    )


@router.get("/participants/{token}/sessions/{session_id}", response_model=SessionResponse)
def get_session(token: str, session_id: UUID, db: Session = Depends(get_db)):
    return get_owned_session(token, session_id, db)
