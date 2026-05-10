import secrets
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.participant import Participant
from app.schemas.participant import ConsentRequest, ParticipantCreate, ParticipantResponse

router = APIRouter(tags=["participants"])


def get_participant_by_token(token: str, db: Session) -> Participant:
    participant = db.query(Participant).filter(Participant.token == token).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return participant


@router.post("/participants", response_model=ParticipantResponse)
def create_participant(data: ParticipantCreate, db: Session = Depends(get_db)):
    participant = Participant(
        token=secrets.token_urlsafe(32),
        metadata_json=data.metadata_json or {},
    )
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant


@router.get("/participants/{token}", response_model=ParticipantResponse)
def get_participant(token: str, db: Session = Depends(get_db)):
    participant = get_participant_by_token(token, db)
    participant.session_count = len(participant.sessions)
    return participant


@router.post("/participants/{token}/consent", response_model=ParticipantResponse)
def record_consent(token: str, data: ConsentRequest, db: Session = Depends(get_db)):
    if not data.agreed:
        raise HTTPException(status_code=400, detail="Consent must be agreed to")
    participant = get_participant_by_token(token, db)
    participant.consent_given_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(participant)
    return participant
