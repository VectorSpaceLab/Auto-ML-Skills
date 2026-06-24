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
    parser.add_argument("--api", choices=["chat", "responses"], default="chat")
    parser.add_argument("--kind", choices=["json", "regex", "choice", "tool", "reasoning"], default="json")
    parser.add_argument("--field-style", choices=["legacy", "structured_outputs"], default="legacy")
    parser.add_argument("--schema", help="Path to JSON schema for --kind json.")
    parser.add_argument("--regex", default=r"\\{.*\\}")
    parser.add_argument("--choice", action="append", default=["yes", "no"])
    parser.add_argument("--prompt", default="Return a city and country as JSON.")
    parser.add_argument("--tool-name", default="lookup_city")
    parser.add_argument("--tool-description", default="Look up city metadata.")
    parser.add_argument("--reasoning-parser", default=None, help="Annotate expected server parser in output metadata.")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    max_token_key = "max_output_tokens" if args.api == "responses" else "max_tokens"
    if args.api == "responses":
        payload = {
            "model": args.model,
            "input": args.prompt,
            "temperature": 0,
            max_token_key: 64,
        }
    else:
        payload = {
            "model": args.model,
            "messages": [{"role": "user", "content": args.prompt}],
            "temperature": 0,
            max_token_key: 64,
        }
    if args.kind == "json":
        schema = json.loads(Path(args.schema).read_text()) if args.schema else default_schema()
        if args.field_style == "structured_outputs":
            payload["structured_outputs"] = {"json": schema}
        else:
            payload["guided_json"] = schema
    elif args.kind == "regex":
        if args.field_style == "structured_outputs":
            payload["structured_outputs"] = {"regex": args.regex}
        else:
            payload["guided_regex"] = args.regex
    elif args.kind == "choice":
        if args.field_style == "structured_outputs":
            payload["structured_outputs"] = {"choice": args.choice}
        else:
            payload["guided_choice"] = args.choice
    elif args.kind == "tool":
        payload["tools"] = [
            {
                "type": "function",
                "function": {
                    "name": args.tool_name,
                    "description": args.tool_description,
                    "parameters": default_schema(),
                },
            }
        ]
        payload["tool_choice"] = "auto"
    else:
        payload["metadata"] = {"expected_reasoning_parser": args.reasoning_parser or "set on server"}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
