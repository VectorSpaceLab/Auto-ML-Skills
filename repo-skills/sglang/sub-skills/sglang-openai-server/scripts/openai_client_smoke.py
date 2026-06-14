#!/usr/bin/env python3
"""Validate a running SGLang OpenAI-compatible server."""

import argparse
import json
import urllib.error
import urllib.request


def get_json(url, timeout=10):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            data = resp.read().decode("utf-8", errors="replace")
            try:
                return {"ok": 200 <= resp.status < 300, "status": resp.status, "body": json.loads(data)}
            except json.JSONDecodeError:
                return {"ok": 200 <= resp.status < 300, "status": resp.status, "body": data}
    except urllib.error.HTTPError as exc:
        data = exc.read().decode("utf-8", errors="replace")
        return {"ok": False, "status": exc.code, "body": data}
    except Exception as exc:
        return {"ok": False, "status": None, "body": f"{type(exc).__name__}: {exc}"}


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
            models = report["models"]["body"]
            model = models["data"][0]["id"] if isinstance(models, dict) and models.get("data") else "default"
        client = OpenAI(base_url=root + "/v1", api_key=args.api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Reply with exactly one short sentence."}],
            max_tokens=16,
            temperature=0,
        )
        report["chat"] = resp.model_dump()

    required = [report["models"].get("ok")]
    if args.chat:
        required.append("chat" in report)
    report["ok"] = all(required)
    print(json.dumps(report, indent=2, default=str))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
