import time
from uuid import UUID
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.conversation import Conversation
from app.routers.sessions import get_owned_session
from app.schemas.conversation import ConversationResponse, ConversationStart, MessageIn
from app.services import experiment as experiment_service
from app.services import llm as llm_service
from app.services.events import log_event

router = APIRouter(tags=["conversations"])


def get_owned_conversation(token: str, session_id: UUID, conv_id: UUID, db: Session) -> Conversation:
    session = get_owned_session(token, session_id, db)
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conv_id, Conversation.session_id == session.id)
        .first()
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.post(
    "/participants/{token}/sessions/{session_id}/conversations",
    response_model=ConversationResponse,
)
def start_conversation(
    token: str, session_id: UUID, data: ConversationStart, db: Session = Depends(get_db)
):
    session = get_owned_session(token, session_id, db)
    if session.completed_at:
        raise HTTPException(status_code=400, detail="Session already completed")

    existing = db.query(Conversation).filter(Conversation.session_id == session.id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Session already has a conversation")

    conversation = Conversation(
        session_id=session.id,
        intent=data.intent,
        topic=data.topic,
        messages=[],
        turn_count=0,
    )
    db.add(conversation)
    log_event(
        db,
        session.participant_id,
        session.id,
        "intent_selected",
        {"intent": data.intent, "topic": data.topic},
    )
    db.commit()
    db.refresh(conversation)
    return conversation


@router.post(
    "/participants/{token}/sessions/{session_id}/conversations/{conv_id}/messages",
    response_model=ConversationResponse,
)
def send_message(
    token: str, session_id: UUID, conv_id: UUID, data: MessageIn, db: Session = Depends(get_db)
):
    conversation = get_owned_conversation(token, session_id, conv_id, db)
    if conversation.completed_at:
        raise HTTPException(status_code=409, detail="Conversation already completed")

    config = experiment_service.load_experiment_config()
    max_turns = config.get("turns_per_conversation", {}).get("max", 5)
    if conversation.turn_count >= max_turns:
        raise HTTPException(status_code=409, detail="Turn limit reached")

    session = conversation.session
    now = datetime.now(timezone.utc)

    messages = list(conversation.messages or [])
    messages.append({"role": "user", "content": data.content, "timestamp": now.isoformat()})
    log_event(
        db,
        session.participant_id,
        session.id,
        "message_sent",
        {"length": len(data.content), "turn": conversation.turn_count + 1},
    )

    started = time.perf_counter()
    result = llm_service.get_claude_response(
        messages=messages, style_profile=session.style_profile
    )
    latency_ms = round((time.perf_counter() - started) * 1000)

    messages.append(
        {
            "role": "assistant",
            "content": result["text"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )
    log_event(
        db,
        session.participant_id,
        session.id,
        "message_received",
        {
            "latency_ms": latency_ms,
            "length": len(result["text"]),
            "stop_reason": result["stop_reason"],
        },
    )

    conversation.messages = messages
    conversation.turn_count = len([m for m in messages if m["role"] == "user"])
    if conversation.turn_count >= max_turns:
        conversation.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(conversation)
    return conversation


@router.get(
    "/participants/{token}/sessions/{session_id}/conversations/{conv_id}",
    response_model=ConversationResponse,
)
def get_conversation(token: str, session_id: UUID, conv_id: UUID, db: Session = Depends(get_db)):
    return get_owned_conversation(token, session_id, conv_id, db)
