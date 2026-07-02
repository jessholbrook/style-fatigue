import uuid

from sqlalchemy import Boolean, Column, DateTime, String, Uuid, func
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.types import JSONVariant


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    token = Column(String(64), unique=True, index=True, nullable=False)
    condition = Column(String(20), nullable=True)
    shift_eligible_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    consent_given_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    metadata_json = Column(JSONVariant, default=dict)

    sessions = relationship("ExperimentSession", back_populates="participant")
    events = relationship("EventLog", back_populates="participant")
