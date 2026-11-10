import secrets
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.participant import Participant
from app.models.session import ExperimentSession
from app.schemas.event import EventIn
from app.schemas.participant import ConsentRequest, ParticipantCreate, ParticipantResponse
from app.services import experiment as experiment_service
from app.services.events import log_event

router = APIRouter(tags=["participants"])


def get_participant_by_token(token: str, db: Session) -> Participant:
    participant = db.query(Participant).filter(Participant.token == token).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return participant


def completed_session_count(participant: Participant, db: Session) -> int:
    return (
        db.query(ExperimentSession)
        .filter(
            ExperimentSession.participant_id == participant.id,
            ExperimentSession.completed_at.isnot(None),
        )
        .count()
    )


def to_participant_response(participant: Participant, db: Session) -> ParticipantResponse:
    return ParticipantResponse.model_validate(participant).model_copy(
        update={"completed_sessions": completed_session_count(participant, db)}
    )


@router.post("/participants", response_model=ParticipantResponse)
def create_participant(data: ParticipantCreate, db: Session = Depends(get_db)):
    # Recruitment pause: blocks new enrollment only. Existing participants keep
    # their links and can finish their remaining sessions.
    if not experiment_service.load_experiment_config().get("enrollment_open", True):
        raise HTTPException(status_code=503, detail={"reason": "enrollment_closed"})
    condition = experiment_service.assign_condition(db)
    participant = Participant(
        token=secrets.token_urlsafe(32),
        condition=condition,
        metadata_json=data.metadata_json or {},
    )
    db.add(participant)
    db.flush()
    log_event(db, participant.id, None, "condition_assigned", {"condition": condition})
    db.commit()
    db.refresh(participant)
    return to_participant_response(participant, db)


@router.get("/participants/{token}", response_model=ParticipantResponse)
def get_participant(token: str, db: Session = Depends(get_db)):
    participant = get_participant_by_token(token, db)
    return to_participant_response(participant, db)


@router.post("/participants/{token}/consent", response_model=ParticipantResponse)
def record_consent(token: str, data: ConsentRequest, db: Session = Depends(get_db)):
    if not data.agreed:
        raise HTTPException(status_code=400, detail="Consent must be agreed to")
    participant = get_participant_by_token(token, db)
    if not participant.consent_given_at:
        participant.consent_given_at = datetime.now(timezone.utc)
        log_event(db, participant.id, None, "consent_given", {})
        db.commit()
        db.refresh(participant)
    return to_participant_response(participant, db)


@router.post("/participants/{token}/events", status_code=204)
def record_event(token: str, data: EventIn, db: Session = Depends(get_db)):
    participant = get_participant_by_token(token, db)
    log_event(
        db,
        participant.id,
        data.session_id,
        data.event_type,
        data.payload,
        data.client_timestamp,
    )
    db.commit()
