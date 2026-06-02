#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def tool_schema() -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": "calculate_gpa",
                "description": "Calculate the Grade Point Average based on grades and credit hours.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "grades": {"type": "array", "items": {"type": "string"}},
                        "hours": {"type": "array", "items": {"type": "integer"}},
                    },
                    "required": ["grades", "hours"],
                },
            },
        }
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=["chat", "toolcall", "image"], required=True)
    parser.add_argument("--prompt", default=None)
    parser.add_argument("--image-url", default="https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen2-VL/boxes.png")
    args = parser.parse_args()
    if args.mode == "chat":
        payload = {"messages": [{"role": "user", "content": args.prompt or "Say hello in one sentence."}]}
    elif args.mode == "toolcall":
        payload = {
            "messages": [
                {"role": "user", "content": args.prompt or "My grades are A, A, B, and C. The credit hours are 3, 4, 3, and 2."}
            ],
            "tools": tool_schema(),
        }
    else:
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": args.prompt or "Output the color and number of each box."},
                        {"type": "image_url", "image_url": {"url": args.image_url}},
                    ],
                }
            ]
        }
    payload["mode"] = args.mode
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
