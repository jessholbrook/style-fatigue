import json
import random
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.conversation import Conversation
from app.models.participant import Participant
from app.models.session import ExperimentSession
from app.services.events import log_event
from app.services.shift import evaluate_shift_readiness


def load_experiment_config() -> dict:
    config_path = Path(get_settings().EXPERIMENT_CONFIG_PATH) / "config.json"
    return json.loads(config_path.read_text())


def assign_condition(db: Session) -> str:
    """Blocked randomization: permuted blocks over the configured conditions.

    Each block's permutation is seeded from SECRET_KEY + block index, so
    assignment is balanced (never off by more than one block), deterministic
    for auditability, and unpredictable to participants.
    """
    config = load_experiment_config()
    conditions = config.get("conditions", ["control", "variant_a", "variant_b"])
    assigned = db.query(Participant).filter(Participant.condition.isnot(None)).count()
    block_index, position = divmod(assigned, len(conditions))
    rng = random.Random(f"{get_settings().SECRET_KEY}:{block_index}")
    block = list(conditions)
    rng.shuffle(block)
    return block[position]


def determine_style_profile(
    participant: Participant, session_number: int, db: Session
) -> tuple[bool, str]:
    """Decide the style profile for a new session.

    Returns (is_shift_session, profile_name). Mutates the participant when the
    trigger fires (stamps shift_eligible_at); the caller owns the commit.

    Controls are evaluated by the same trigger and stamped at the same moment
    (pseudo-shift marker) so detection windows align across arms — they just
    stay on baseline.
    """
    config = load_experiment_config()

    if participant.shift_eligible_at:
        if participant.condition == "control":
            return False, "baseline"
        return False, participant.condition

    if session_number <= config.get("min_sessions_before_shift", 2):
        return False, "baseline"

    metrics = evaluate_shift_readiness(participant.id, db)
    if metrics is None:
        return False, "baseline"

    participant.shift_eligible_at = datetime.now(timezone.utc)
    log_event(
        db,
        participant.id,
        None,
        "shift_triggered",
        {"condition": participant.condition, **metrics},
    )
    if participant.condition == "control":
        return False, "baseline"
    return True, participant.condition


def get_available_intents(participant: Participant, db: Session) -> dict:
    """Intent menu with this participant's already-used topics filtered out."""
    intents_path = Path(get_settings().EXPERIMENT_CONFIG_PATH) / "intents.json"
    data = json.loads(intents_path.read_text())

    used_topics = {
        topic
        for (topic,) in db.query(Conversation.topic)
        .join(ExperimentSession, Conversation.session_id == ExperimentSession.id)
        .filter(ExperimentSession.participant_id == participant.id)
        .all()
    }

    intents = []
    for intent in data["intents"]:
        topics = [t for t in intent["topics"] if t not in used_topics]
        if topics:
            intents.append({**intent, "topics": topics})
    return {"intents": intents}
