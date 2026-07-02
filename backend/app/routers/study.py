from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers.participants import get_participant_by_token
from app.services import experiment as experiment_service

router = APIRouter(tags=["study"])


@router.get("/config")
def get_public_config():
    """Public subset of the experiment config — never the shift criteria."""
    config = experiment_service.load_experiment_config()
    return {
        "max_sessions": config.get("max_sessions", 6),
        "turns_per_conversation": config.get("turns_per_conversation", {"min": 3, "max": 5}),
        "session_cooldown_hours": config.get("session_cooldown_hours", 48),
    }


@router.get("/participants/{token}/intents")
def get_intents(token: str, db: Session = Depends(get_db)):
    participant = get_participant_by_token(token, db)
    return experiment_service.get_available_intents(participant, db)
