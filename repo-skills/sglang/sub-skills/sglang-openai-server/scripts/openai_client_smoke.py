#!/usr/bin/env python3
"""Validate a running SGLang OpenAI-compatible server."""

import argparse
import json
import urllib.request


def get_json(url, timeout=10):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        data = resp.read().decode("utf-8", errors="replace")
        try:
            return resp.status, json.loads(data)
        except json.JSONDecodeError:
            return resp.status, data


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke test health/models and optional chat on an SGLang server.")
    parser.add_argument("--base-url", default="http://127.0.0.1:30000", help="Server root, not /v1.")
    parser.add_argument("--model", default=None, help="Model name for optional chat request.")
    parser.add_argument("--chat", action="store_true", help="Send a chat.completions request.")
    parser.add_argument("--api-key", default="None")
    args = parser.parse_args()

    root = args.base_url.rstrip("/")
    report = {}
    report["health"] = get_json(root + "/health")
    report["models"] = get_json(root + "/v1/models")

    if args.chat:
        from openai import OpenAI

        model = args.model
        if model is None:
            models = report["models"][1]
            model = models["data"][0]["id"] if isinstance(models, dict) and models.get("data") else "default"
        client = OpenAI(base_url=root + "/v1", api_key=args.api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Reply with exactly one short sentence."}],
            max_tokens=16,
            temperature=0,
        )
        report["chat"] = resp.model_dump()

    print(json.dumps(report, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
