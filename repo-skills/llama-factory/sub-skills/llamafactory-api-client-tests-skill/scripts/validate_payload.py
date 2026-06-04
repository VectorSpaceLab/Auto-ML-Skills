#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.payload.read_text(encoding="utf-8"))
    errors: list[str] = []
    messages = payload.get("messages")
    if not isinstance(messages, list) or not messages:
        errors.append("messages must be a non-empty list")
    else:
        for idx, msg in enumerate(messages):
            if msg.get("role") not in {"system", "user", "assistant", "tool"}:
                errors.append(f"message {idx} has invalid role")
            if "content" not in msg:
                errors.append(f"message {idx} has no content")
    mode = payload.get("mode")
    if mode == "toolcall":
        tools = payload.get("tools")
        if not isinstance(tools, list) or not tools:
            errors.append("toolcall mode requires tools")
    if mode == "image":
        content = messages[0].get("content") if messages else None
        has_image = isinstance(content, list) and any(part.get("type") == "image_url" for part in content if isinstance(part, dict))
        if not has_image:
            errors.append("image mode requires an image_url content part")
    print(f"mode: {mode}")
    print(f"messages: {len(messages) if isinstance(messages, list) else 0}")
    print(f"tools: {len(payload.get('tools', [])) if isinstance(payload.get('tools', []), list) else 0}")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
