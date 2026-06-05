#!/usr/bin/env python3
"""Create OpenAI-style JSONL batch requests for vLLM run-batch."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="Qwen/Qwen3-0.6B")
    parser.add_argument("--mode", choices=["chat", "completion"], default="chat")
    parser.add_argument("--prompt", action="append", default=["Say hello."])
    parser.add_argument("--max-tokens", type=int, default=16)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        for i, prompt in enumerate(args.prompt):
            if args.mode == "chat":
                body = {
                    "model": args.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0,
                    "max_tokens": args.max_tokens,
                }
                url = "/v1/chat/completions"
            else:
                body = {
                    "model": args.model,
                    "prompt": prompt,
                    "temperature": 0,
                    "max_tokens": args.max_tokens,
                }
                url = "/v1/completions"
            handle.write(json.dumps({"custom_id": f"request-{i}", "method": "POST", "url": url, "body": body}) + "\n")
    print(str(out))


if __name__ == "__main__":
    main()
