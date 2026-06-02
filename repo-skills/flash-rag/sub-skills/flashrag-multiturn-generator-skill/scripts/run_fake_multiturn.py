#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import read_simple_yaml


def render(messages: list[dict]) -> str:
    return "\n".join(f"{msg['role'].upper()}: {msg['content']}" for msg in messages) + "\nASSISTANT:"


def fake_answer(prompt: str, turn_idx: int) -> str:
    if "Hamlet" in prompt and turn_idx == 1:
        return "William Shakespeare."
    if "surname" in prompt.lower():
        return "Shakespeare."
    return f"Fake answer for turn {turn_idx}."


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--messages", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    config = read_simple_yaml(args.config)
    raw_messages = json.loads(args.messages.read_text(encoding="utf-8"))
    base = [m for m in raw_messages if m["role"] == "system"]
    turns = [m for m in raw_messages if m["role"] == "user"]
    transcript = list(base)
    records = []
    for idx, user_msg in enumerate(turns, start=1):
        transcript.append(user_msg)
        prompt = render(transcript)
        output = fake_answer(prompt, idx)
        transcript.append({"role": "assistant", "content": output})
        records.append({"turn": idx, "prompt": prompt, "output": output})
    result = {
        "save_dir": config.get("save_dir"),
        "turns": len(records),
        "records": records,
        "final_messages": transcript,
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"valid: {str(len(records) > 0 and bool(records[-1]['output'])).lower()}")
    return 0 if records else 1


if __name__ == "__main__":
    raise SystemExit(main())
