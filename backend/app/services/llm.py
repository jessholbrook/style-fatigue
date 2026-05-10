import json
from pathlib import Path

import anthropic

from app.config import get_settings


def load_style_profile(profile_name: str) -> dict:
    profile_path = Path(get_settings().EXPERIMENT_CONFIG_PATH) / "style_profiles" / f"{profile_name}.json"
    return json.loads(profile_path.read_text())


def build_system_prompt(profile: dict) -> str:
    parts = [profile["system_prompt"]]
    if profile.get("few_shot_instructions"):
        parts.append(profile["few_shot_instructions"])
    return "\n\n".join(parts)


def get_claude_response(messages: list[dict], style_profile: str) -> str:
    settings = get_settings()
    profile = load_style_profile(style_profile)
    config_path = Path(settings.EXPERIMENT_CONFIG_PATH) / "config.json"
    experiment_config = json.loads(config_path.read_text())

    system_prompt = build_system_prompt(profile)

    api_messages = []
    for msg in messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=experiment_config.get("model", "claude-sonnet-4-20250514"),
        max_tokens=1024,
        system=system_prompt,
        messages=api_messages,
    )
    return response.content[0].text
