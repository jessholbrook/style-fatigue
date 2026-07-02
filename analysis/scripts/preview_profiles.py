"""Manipulation check: generate side-by-side sample responses per style profile.

Run this before piloting to verify the three profiles are perceptibly distinct
and that variant outputs are not being truncated (stop_reason).

    ANTHROPIC_API_KEY=... python preview_profiles.py [--samples 2]
"""

import argparse
import json
import os
from pathlib import Path

import anthropic

REPO_ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_DIR = Path(os.environ.get("EXPERIMENT_CONFIG_PATH", REPO_ROOT / "experiment"))
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "output" / "profile_preview.md"

PREVIEW_PROMPTS = [
    "What's a good way to start learning guitar?",
    "Can you explain how compound interest works?",
    "Help me brainstorm ideas for a friend's birthday party.",
    "I keep waking up at 3am and can't fall back asleep. Any advice?",
]


def load_profiles() -> dict[str, dict]:
    profiles = {}
    for path in sorted((EXPERIMENT_DIR / "style_profiles").glob("*.json")):
        profile = json.loads(path.read_text())
        profiles[profile["name"]] = profile
    return profiles


def build_system_prompt(profile: dict) -> str:
    parts = [profile["system_prompt"]]
    if profile.get("few_shot_instructions"):
        parts.append(profile["few_shot_instructions"])
    return "\n\n".join(parts)


def generate(client: anthropic.Anthropic, config: dict, profile: dict, prompt: str) -> dict:
    messages = [
        {"role": m["role"], "content": m["content"]}
        for m in profile.get("few_shot_examples", [])
    ]
    messages.append({"role": "user", "content": prompt})
    response = client.messages.create(
        model=config.get("model", "claude-sonnet-4-20250514"),
        max_tokens=config.get("max_tokens", 2048),
        temperature=config.get("temperature", 1.0),
        system=build_system_prompt(profile),
        messages=messages,
    )
    return {"text": response.content[0].text, "stop_reason": response.stop_reason}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=1, help="samples per prompt per profile")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("Set ANTHROPIC_API_KEY to run the preview.")

    config = json.loads((EXPERIMENT_DIR / "config.json").read_text())
    profiles = load_profiles()
    client = anthropic.Anthropic(api_key=api_key)

    lines = ["# Style Profile Preview\n"]
    truncations = 0
    for prompt in PREVIEW_PROMPTS:
        lines.append(f"\n## Prompt: {prompt}\n")
        for name, profile in profiles.items():
            for i in range(args.samples):
                print(f"{name} / sample {i + 1} / {prompt[:40]}...")
                result = generate(client, config, profile, prompt)
                if result["stop_reason"] != "end_turn":
                    truncations += 1
                lines.append(f"\n### {name} (sample {i + 1}, stop: {result['stop_reason']})\n")
                lines.append(result["text"])
                lines.append("\n---")

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines))
    print(f"\nWrote {OUTPUT_PATH}")
    if truncations:
        print(f"WARNING: {truncations} responses did not stop at end_turn — check max_tokens.")


if __name__ == "__main__":
    main()
