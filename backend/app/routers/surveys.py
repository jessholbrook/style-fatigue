import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models.survey_response import SurveyResponse
from app.schemas.survey import SurveyResponseOut, SurveySubmission

router = APIRouter(tags=["surveys"])


@router.get("/surveys/{survey_type}")
def get_survey_instrument(survey_type: str):
    config_path = Path(get_settings().EXPERIMENT_CONFIG_PATH) / "survey_instruments" / f"{survey_type}.json"
    if not config_path.exists():
        raise HTTPException(status_code=404, detail=f"Survey type '{survey_type}' not found")
    return json.loads(config_path.read_text())


@router.post("/sessions/{session_id}/surveys", response_model=SurveyResponseOut)
def submit_survey(session_id: str, data: SurveySubmission, db: Session = Depends(get_db)):
    noticeability = data.responses.get("notice_change")
    preference = data.responses.get("preference")

    survey = SurveyResponse(
        session_id=session_id,
        survey_type=data.survey_type,
        responses=data.responses,
        noticeability_score=int(noticeability) if noticeability is not None else None,
        preference_score=int(preference) if preference is not None else None,
        free_text=data.free_text,
    )
    db.add(survey)
    db.commit()
    db.refresh(survey)
    return survey
