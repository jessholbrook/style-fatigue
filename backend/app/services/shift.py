import json
from pathlib import Path
from statistics import fmean, pvariance
from uuid import UUID

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.session import ExperimentSession
from app.models.survey_response import SurveyResponse


def load_shift_criteria() -> dict:
    config_path = Path(get_settings().EXPERIMENT_CONFIG_PATH) / "config.json"
    config = json.loads(config_path.read_text())
    return config.get("shift_criteria", {})


def evaluate_shift_readiness(participant_id: UUID, db: Session) -> dict | None:
    """Return the trigger metrics if the participant has habituated, else None.

    Habituation = across the last N *distinct* sessions: noticeability is both
    stable (low variance) and low (low mean), and preference is stable. A
    stability-only criterion would shift someone consistently rating the style
    "extremely different" (7,7,7), which is the opposite of habituation.
    """
    criteria = load_shift_criteria()
    notice_window = criteria.get("noticeability_stability_window", 3)
    pref_window = criteria.get("preference_stability_window", 3)
    max_notice_var = criteria.get("noticeability_max_variance", 1.0)
    max_notice_mean = criteria.get("noticeability_max_mean", 3.0)
    max_pref_var = criteria.get("preference_max_variance", 1.5)

    rows = (
        db.query(SurveyResponse, ExperimentSession.session_number)
        .join(ExperimentSession, SurveyResponse.session_id == ExperimentSession.id)
        .filter(ExperimentSession.participant_id == participant_id)
        .filter(SurveyResponse.survey_type == "post_conversation")
        .order_by(ExperimentSession.session_number.desc(), SurveyResponse.submitted_at.asc())
        .all()
    )

    # One survey per session: duplicates must not fill the stability window.
    by_session: dict[int, SurveyResponse] = {}
    for survey, session_number in rows:
        by_session.setdefault(session_number, survey)
    ordered = [by_session[n] for n in sorted(by_session, reverse=True)]

    notice_scores = [
        s.noticeability_score for s in ordered[:notice_window] if s.noticeability_score is not None
    ]
    pref_scores = [
        s.preference_score for s in ordered[:pref_window] if s.preference_score is not None
    ]

    if len(notice_scores) < notice_window or len(pref_scores) < pref_window:
        return None

    notice_variance = pvariance(notice_scores)
    notice_mean = fmean(notice_scores)
    pref_variance = pvariance(pref_scores)

    ready = (
        notice_variance <= max_notice_var
        and notice_mean <= max_notice_mean
        and pref_variance <= max_pref_var
    )
    if not ready:
        return None

    return {
        "notice_scores": notice_scores,
        "notice_variance": notice_variance,
        "notice_mean": notice_mean,
        "pref_scores": pref_scores,
        "pref_variance": pref_variance,
        "sessions_observed": len(ordered),
    }
