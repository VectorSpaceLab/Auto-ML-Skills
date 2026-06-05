#!/usr/bin/env python3
"""Lint OpenAI-style multimodal message content."""

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a JSON file containing OpenAI chat messages with multimodal content.")
    parser.add_argument("json_file", nargs="?", help="Path to JSON payload or messages array.")
    args = parser.parse_args()
    if not args.json_file:
        print("Provide a JSON file to validate; --help is lightweight.")
        return 0
    data = json.load(open(args.json_file, encoding="utf-8"))
    messages = data.get("messages", data) if isinstance(data, dict) else data
    issues = []
    if not isinstance(messages, list):
        issues.append("messages must be a list")
    else:
        for i, msg in enumerate(messages):
            if "role" not in msg:
                issues.append(f"message {i} missing role")
            content = msg.get("content")
            if isinstance(content, list):
                for j, part in enumerate(content):
                    if part.get("type") == "image_url" and "image_url" not in part:
                        issues.append(f"message {i} part {j} image_url missing image_url object")
                    if part.get("type") == "text" and "text" not in part:
                        issues.append(f"message {i} part {j} text missing text field")
    print(json.dumps({"ok": not issues, "issues": issues}, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
