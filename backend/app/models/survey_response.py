import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Uuid, func
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.types import JSONVariant


class SurveyResponse(Base):
    __tablename__ = "survey_responses"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    session_id = Column(Uuid, ForeignKey("sessions.id"), nullable=False)
    survey_type = Column(String(30), nullable=False)
    responses = Column(JSONVariant, default=dict)
    noticeability_score = Column(Integer, nullable=True)
    preference_score = Column(Integer, nullable=True)
    free_text = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("ExperimentSession", back_populates="survey_responses")
