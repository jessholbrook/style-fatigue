import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class ExperimentSession(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    participant_id = Column(UUID(as_uuid=True), ForeignKey("participants.id"), nullable=False)
    session_number = Column(Integer, nullable=False)
    style_profile = Column(String(20), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    is_shift_session = Column(Boolean, default=False)

    participant = relationship("Participant", back_populates="sessions")
    conversations = relationship("Conversation", back_populates="session")
    survey_responses = relationship("SurveyResponse", back_populates="session")
    events = relationship("EventLog", back_populates="session")
