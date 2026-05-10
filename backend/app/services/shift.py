import json
from pathlib import Path
from uuid import UUID

import numpy as np
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.session import ExperimentSession
from app.models.survey_response import SurveyResponse


def load_shift_criteria() -> dict:
    config_path = Path(get_settings().EXPERIMENT_CONFIG_PATH) / "config.json"
    config = json.loads(config_path.read_text())
    return config.get("shift_criteria", {})


def evaluate_shift_readiness(participant_id: UUID, db: Session) -> bool:
    criteria = load_shift_criteria()
    window = criteria.get("noticeability_stability_window", 2)
    max_notice_var = criteria.get("noticeability_max_variance", 1.0)
    max_pref_var = criteria.get("preference_max_variance", 1.5)

    recent_surveys = (
        db.query(SurveyResponse)
        .join(ExperimentSession, SurveyResponse.session_id == ExperimentSession.id)
        .filter(ExperimentSession.participant_id == participant_id)
        .filter(SurveyResponse.survey_type == "post_conversation")
        .order_by(ExperimentSession.session_number.desc())
        .limit(window)
        .all()
    )

    if len(recent_surveys) < window:
        return False

    notice_scores = [s.noticeability_score for s in recent_surveys if s.noticeability_score is not None]
    pref_scores = [s.preference_score for s in recent_surveys if s.preference_score is not None]

    if len(notice_scores) < window or len(pref_scores) < window:
        return False

    notice_stable = np.var(notice_scores) <= max_notice_var
    pref_stable = np.var(pref_scores) <= max_pref_var

    return notice_stable and pref_stable
