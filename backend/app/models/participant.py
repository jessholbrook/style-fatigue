import uuid

from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Participant(Base):
    __tablename__ = "participants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(String(64), unique=True, index=True, nullable=False)
    condition = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    consent_given_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    metadata_json = Column(JSONB, default=dict)

    sessions = relationship("ExperimentSession", back_populates="participant")
    events = relationship("EventLog", back_populates="participant")
