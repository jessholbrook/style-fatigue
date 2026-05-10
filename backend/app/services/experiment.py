import json
import random
from pathlib import Path

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.participant import Participant
from app.services.shift import evaluate_shift_readiness


def load_experiment_config() -> dict:
    config_path = Path(get_settings().EXPERIMENT_CONFIG_PATH) / "config.json"
    return json.loads(config_path.read_text())


def assign_condition(participant: Participant, db: Session) -> str:
    condition = random.choice(["variant_a", "variant_b"])
    participant.condition = condition
    db.commit()
    return condition


def determine_style_profile(
    participant: Participant, session_number: int, db: Session
) -> tuple[bool, str]:
    config = load_experiment_config()

    if participant.condition:
        return False, participant.condition

    min_sessions = config.get("min_sessions_before_shift", 2)
    if session_number <= min_sessions:
        return False, "baseline"

    if evaluate_shift_readiness(participant.id, db):
        condition = assign_condition(participant, db)
        return True, condition

    return False, "baseline"


def check_shift_eligibility(participant: Participant, db: Session) -> bool:
    if participant.condition:
        return False
    return evaluate_shift_readiness(participant.id, db)


def get_available_intents() -> dict:
    intents_path = Path(get_settings().EXPERIMENT_CONFIG_PATH) / "intents.json"
    return json.loads(intents_path.read_text())
