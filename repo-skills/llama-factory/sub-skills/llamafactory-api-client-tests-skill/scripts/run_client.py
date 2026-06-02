#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def calculate_gpa(grades: list[str], hours: list[int]) -> float:
    score = {"A": 4, "B": 3, "C": 2, "D": 1, "F": 0}
    total_score = sum(score[g] * h for g, h in zip(grades, hours))
    total_hours = sum(hours)
    return round(total_score / total_hours, 2)


def offline_response(payload: dict[str, Any]) -> dict[str, Any]:
    mode = payload.get("mode")
    if mode == "toolcall":
        args = {"grades": ["A", "A", "B", "C"], "hours": [3, 4, 3, 2]}
        return {
            "tool_call": {"name": "calculate_gpa", "arguments": args},
            "tool_result": {"gpa": calculate_gpa(**args)},
            "final": "Based on the provided grades and credit hours, the GPA is 3.42.",
        }
    if mode == "image":
        return {"final": "Offline mock accepted an image_url multimodal payload."}
    return {"final": "Offline mock chat response."}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload", type=Path, required=True)
    parser.add_argument("--base-url", default="http://localhost:8000/v1")
    parser.add_argument("--api-key", default="0")
    parser.add_argument("--model", default="test")
    parser.add_argument("--offline-mock", action="store_true")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    payload = json.loads(args.payload.read_text(encoding="utf-8"))
    mode = payload.pop("mode", None)
    if args.offline_mock:
        result = {"mode": mode, "base_url": args.base_url, "model": args.model, **offline_response({"mode": mode, **payload})}
    else:
        from openai import OpenAI

        client = OpenAI(api_key=args.api_key, base_url=args.base_url)
        kwargs = {"model": args.model, "messages": payload["messages"]}
        if payload.get("tools"):
            kwargs["tools"] = payload["tools"]
        response = client.chat.completions.create(**kwargs)
        message = response.choices[0].message
        result = {
            "mode": mode,
            "content": message.content,
            "tool_calls": [
                {"name": call.function.name, "arguments": json.loads(call.function.arguments)}
                for call in (message.tool_calls or [])
            ],
        }
        if result["tool_calls"]:
            call = result["tool_calls"][0]
            if call["name"] == "calculate_gpa":
                result["tool_result"] = {"gpa": calculate_gpa(**call["arguments"])}
                result["followup_tool_message"] = {
                    "role": "tool",
                    "content": json.dumps(result["tool_result"], ensure_ascii=False),
                }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ok = bool(result.get("final") or result.get("content") or result.get("tool_calls"))
    print(f"valid: {str(ok).lower()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
