import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Uuid, func
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.types import JSONVariant


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    session_id = Column(Uuid, ForeignKey("sessions.id"), nullable=False)
    intent = Column(String(100), nullable=False)
    topic = Column(String(100), nullable=False)
    messages = Column(JSONVariant, default=list)
    turn_count = Column(Integer, default=0)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    session = relationship("ExperimentSession", back_populates="conversations")
