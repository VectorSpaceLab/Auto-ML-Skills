#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def _request(url: str, payload: dict[str, Any] | None = None, api_key: str | None = None) -> tuple[int, str]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="GET" if payload is None else "POST")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, resp.read().decode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check LLaMA-Factory OpenAI-compatible API endpoints.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--prompt", default="Say hello in one short sentence.")
    parser.add_argument("--model", default="llamafactory-local")
    parser.add_argument("--max-tokens", type=int, default=16)
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    deadline = time.time() + args.timeout
    last_error = ""
    models_body = ""
    while time.time() < deadline:
        try:
            status, models_body = _request(f"{args.base_url}/v1/models", api_key=args.api_key)
            if status == 200:
                break
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            time.sleep(2)
    else:
        print("valid: false")
        print(f"- /v1/models did not become ready: {last_error}")
        return 1

    payload = {
        "model": args.model,
        "messages": [{"role": "user", "content": args.prompt}],
        "max_tokens": args.max_tokens,
        "stream": False,
        "temperature": 0.0,
    }
    try:
        status, body = _request(f"{args.base_url}/v1/chat/completions", payload, api_key=args.api_key)
    except Exception as exc:
        print("valid: false")
        print(f"- chat completion failed: {type(exc).__name__}: {exc}")
        return 1

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(body + "\n", encoding="utf-8")
    data = json.loads(body)
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    print(f"models: {models_body}")
    print(f"status: {status}")
    print(f"response: {content}")
    ok = status == 200 and bool(content)
    print(f"valid: {str(ok).lower()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
