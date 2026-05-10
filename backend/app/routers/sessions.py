from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.session import ExperimentSession
from app.routers.participants import get_participant_by_token
from app.schemas.session import SessionResponse
from app.services.experiment import determine_style_profile, check_shift_eligibility

router = APIRouter(tags=["sessions"])


@router.post("/participants/{token}/sessions", response_model=SessionResponse)
def start_session(token: str, db: Session = Depends(get_db)):
    participant = get_participant_by_token(token, db)
    if not participant.consent_given_at:
        raise HTTPException(status_code=400, detail="Consent required before starting sessions")

    existing = (
        db.query(ExperimentSession)
        .filter(ExperimentSession.participant_id == participant.id)
        .order_by(ExperimentSession.session_number.desc())
        .first()
    )
    if existing and not existing.completed_at:
        raise HTTPException(status_code=400, detail="Previous session not yet completed")

    next_number = (existing.session_number + 1) if existing else 1
    is_shift, style_profile = determine_style_profile(participant, next_number, db)

    session = ExperimentSession(
        participant_id=participant.id,
        session_number=next_number,
        style_profile=style_profile,
        is_shift_session=is_shift,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


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
def get_session(token: str, session_id: str, db: Session = Depends(get_db)):
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


@router.post("/participants/{token}/sessions/{session_id}/complete", response_model=SessionResponse)
def complete_session(token: str, session_id: str, db: Session = Depends(get_db)):
    from datetime import datetime, timezone

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

    session.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(session)
    return session
