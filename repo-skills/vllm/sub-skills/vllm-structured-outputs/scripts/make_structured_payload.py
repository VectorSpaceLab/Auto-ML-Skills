#!/usr/bin/env python3
"""Create a vLLM OpenAI-compatible structured-output request payload."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def default_schema() -> dict:
    return {
        "type": "object",
        "properties": {"city": {"type": "string"}, "country": {"type": "string"}},
        "required": ["city", "country"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="Qwen/Qwen3-0.6B")
    parser.add_argument("--kind", choices=["json", "regex", "choice"], default="json")
    parser.add_argument("--schema", help="Path to JSON schema for --kind json.")
    parser.add_argument("--regex", default=r"\\{.*\\}")
    parser.add_argument("--choice", action="append", default=["yes", "no"])
    parser.add_argument("--prompt", default="Return a city and country as JSON.")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    payload = {
        "model": args.model,
        "messages": [{"role": "user", "content": args.prompt}],
        "temperature": 0,
        "max_tokens": 64,
    }
    if args.kind == "json":
        payload["guided_json"] = json.loads(Path(args.schema).read_text()) if args.schema else default_schema()
    elif args.kind == "regex":
        payload["guided_regex"] = args.regex
    else:
        payload["guided_choice"] = args.choice
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
