from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.conversation import Conversation
from app.models.session import ExperimentSession
from app.schemas.conversation import ConversationResponse, ConversationStart, MessageIn, MessageOut
from app.services.llm import get_claude_response

router = APIRouter(tags=["conversations"])


@router.post("/sessions/{session_id}/conversations", response_model=ConversationResponse)
def start_conversation(session_id: str, data: ConversationStart, db: Session = Depends(get_db)):
    session = db.query(ExperimentSession).filter(ExperimentSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    existing = db.query(Conversation).filter(Conversation.session_id == session.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Session already has a conversation")

    conversation = Conversation(
        session_id=session.id,
        intent=data.intent,
        topic=data.topic,
        messages=[],
        turn_count=0,
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


@router.post("/sessions/{session_id}/conversations/{conv_id}/messages", response_model=ConversationResponse)
def send_message(session_id: str, conv_id: str, data: MessageIn, db: Session = Depends(get_db)):
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conv_id, Conversation.session_id == session_id)
        .first()
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conversation.completed_at:
        raise HTTPException(status_code=400, detail="Conversation already completed")

    session = db.query(ExperimentSession).filter(ExperimentSession.id == session_id).first()
    now = datetime.now(timezone.utc).isoformat()

    messages = list(conversation.messages or [])
    messages.append({"role": "user", "content": data.content, "timestamp": now})

    assistant_content = get_claude_response(
        messages=messages,
        style_profile=session.style_profile,
    )
    messages.append({"role": "assistant", "content": assistant_content, "timestamp": datetime.now(timezone.utc).isoformat()})

    conversation.messages = messages
    conversation.turn_count = len([m for m in messages if m["role"] == "user"])
    db.commit()
    db.refresh(conversation)
    return conversation


@router.get("/sessions/{session_id}/conversations/{conv_id}", response_model=ConversationResponse)
def get_conversation(session_id: str, conv_id: str, db: Session = Depends(get_db)):
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conv_id, Conversation.session_id == session_id)
        .first()
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation
