from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Uuid, func
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.types import JSONVariant


class EventLog(Base):
    __tablename__ = "event_log"

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    participant_id = Column(Uuid, ForeignKey("participants.id"), index=True)
    session_id = Column(Uuid, ForeignKey("sessions.id"), nullable=True, index=True)
    event_type = Column(String(50), nullable=False, index=True)
    payload = Column(JSONVariant, default=dict)
    client_timestamp = Column(DateTime(timezone=True), nullable=True)
    server_timestamp = Column(DateTime(timezone=True), server_default=func.now())

    participant = relationship("Participant", back_populates="events")
    session = relationship("ExperimentSession", back_populates="events")
