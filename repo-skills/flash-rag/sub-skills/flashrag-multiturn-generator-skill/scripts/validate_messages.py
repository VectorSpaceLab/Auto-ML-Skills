#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--messages", type=Path, required=True)
    args = parser.parse_args()
    messages = json.loads(args.messages.read_text(encoding="utf-8"))
    errors: list[str] = []
    if not isinstance(messages, list) or not messages:
        errors.append("messages must be a non-empty list")
    roles = []
    for idx, msg in enumerate(messages if isinstance(messages, list) else []):
        role = msg.get("role")
        roles.append(role)
        if role not in {"system", "user", "assistant", "tool"}:
            errors.append(f"message {idx} has invalid role")
        if not str(msg.get("content", "")).strip():
            errors.append(f"message {idx} has empty content")
    if roles and roles[0] not in {"system", "user"}:
        errors.append("first message should be system or user")
    user_count = roles.count("user")
    if user_count < 1:
        errors.append("at least one user turn is required")
    print(f"messages: {len(messages) if isinstance(messages, list) else 0}")
    print(f"user_turns: {user_count}")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
