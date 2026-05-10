from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SurveySubmission(BaseModel):
    survey_type: str
    responses: dict
    free_text: str | None = None


class SurveyResponseOut(BaseModel):
    id: UUID
    survey_type: str
    responses: dict
    noticeability_score: int | None
    preference_score: int | None
    free_text: str | None
    submitted_at: datetime

    model_config = {"from_attributes": True}
