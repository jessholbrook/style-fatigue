import json
from uuid import UUID
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models.survey_response import SurveyResponse
from app.routers.participants import completed_session_count, get_participant_by_token
from app.routers.sessions import get_owned_session
from app.schemas.survey import SurveySubmission, SurveySubmitResponse
from app.services import experiment as experiment_service
from app.services.events import log_event

router = APIRouter(tags=["surveys"])

# Allowlist: the path segment must never reach the filesystem unchecked
# (path traversal would leak config.json, i.e. the shift criteria).
SURVEY_TYPES = {"post_conversation", "exit_survey"}


@router.get("/surveys/{survey_type}")
def get_survey_instrument(survey_type: str):
    if survey_type not in SURVEY_TYPES:
        raise HTTPException(status_code=404, detail="Survey type not found")
    config_path = (
        Path(get_settings().EXPERIMENT_CONFIG_PATH) / "survey_instruments" / f"{survey_type}.json"
    )
    return json.loads(config_path.read_text())


@router.post(
    "/participants/{token}/sessions/{session_id}/surveys",
    response_model=SurveySubmitResponse,
)
def submit_survey(
    token: str, session_id: UUID, data: SurveySubmission, db: Session = Depends(get_db)
):
    participant = get_participant_by_token(token, db)
    session = get_owned_session(token, session_id, db)

    existing = (
        db.query(SurveyResponse)
        .filter(
            SurveyResponse.session_id == session.id,
            SurveyResponse.survey_type == data.survey_type,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Survey already submitted for this session")

    survey = SurveyResponse(
        session_id=session.id,
        survey_type=data.survey_type,
        responses=data.responses,
        noticeability_score=data.responses.get("notice_change"),
        preference_score=data.responses.get("preference"),
        free_text=data.free_text,
    )
    db.add(survey)

    # The post-conversation survey is the last step of a session — completing
    # it server-side is what unlocks the next session.
    if data.survey_type == "post_conversation" and not session.completed_at:
        session.completed_at = datetime.now(timezone.utc)

    log_event(
        db,
        participant.id,
        session.id,
        "survey_submitted",
        {"survey_type": data.survey_type},
    )
    db.commit()
    db.refresh(survey)

    config = experiment_service.load_experiment_config()
    study_complete = completed_session_count(participant, db) >= config.get("max_sessions", 6)

    return SurveySubmitResponse(
        id=survey.id,
        submitted_at=survey.submitted_at,
        study_complete=study_complete,
    )
