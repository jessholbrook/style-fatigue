from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, field_validator

LIKERT_IDS = ("notice_change", "preference")


class SurveySubmission(BaseModel):
    survey_type: Literal["post_conversation", "exit_survey"]
    responses: dict
    free_text: str | None = None

    @field_validator("responses")
    @classmethod
    def validate_likert_scores(cls, v: dict) -> dict:
        for key in LIKERT_IDS:
            score = v.get(key)
            if score is not None and (not isinstance(score, int) or not 1 <= score <= 7):
                raise ValueError(f"{key} must be an integer between 1 and 7")
        return v


class SurveySubmitResponse(BaseModel):
    id: UUID
    submitted_at: datetime
    study_complete: bool = False
