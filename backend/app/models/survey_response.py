import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.database import Base


class SurveyResponse(Base):
    __tablename__ = "survey_responses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    survey_type = Column(String(30), nullable=False)
    responses = Column(JSONB, default=dict)
    noticeability_score = Column(Integer, nullable=True)
    preference_score = Column(Integer, nullable=True)
    free_text = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("ExperimentSession", back_populates="survey_responses")
