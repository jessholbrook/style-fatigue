from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.database import Base


class EventLog(Base):
    __tablename__ = "event_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    participant_id = Column(UUID(as_uuid=True), ForeignKey("participants.id"), index=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=True, index=True)
    event_type = Column(String(50), nullable=False, index=True)
    payload = Column(JSONB, default=dict)
    client_timestamp = Column(DateTime(timezone=True), nullable=True)
    server_timestamp = Column(DateTime(timezone=True), server_default=func.now())

    participant = relationship("Participant", back_populates="events")
    session = relationship("ExperimentSession", back_populates="events")
