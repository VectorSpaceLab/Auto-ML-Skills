#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import tiktoken


def prompt_text(prompt) -> str:
    if isinstance(prompt, list):
        return "\n".join(str(message.get("content", "")) for message in prompt)
    return str(prompt)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt-output", type=Path, required=True)
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("--encoding-model", default="gpt-3.5-turbo")
    args = parser.parse_args()

    errors: list[str] = []
    payload = json.loads(args.prompt_output.read_text(encoding="utf-8"))
    prompt = payload.get("prompt")
    text = prompt_text(prompt)
    encoder = tiktoken.encoding_for_model(args.encoding_model)
    token_count = len(encoder.encode(text))

    print(f"prompt_output: {args.prompt_output.resolve()}")
    print(f"prompt_type: {payload.get('prompt_type')}")
    print(f"doc_count: {payload.get('doc_count')}")
    print(f"chars: {len(text)}")
    print(f"tokens: {token_count}")
    print(f"question_present: {str(str(payload.get('question', '')) in text).lower()}")
    has_reference = bool(payload.get("formatted_reference") or payload.get("compressed_reference") or "Doc 1" in text)
    print(f"reference_present: {str(has_reference).lower()}")
    if not text.strip():
        errors.append("prompt is empty")
    if payload.get("question") and str(payload["question"]) not in text:
        errors.append("question not found in prompt")
    if not has_reference:
        errors.append("reference text not found")
    if args.max_tokens is not None and token_count > args.max_tokens:
        errors.append(f"token count {token_count} exceeds max {args.max_tokens}")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
