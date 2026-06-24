#!/usr/bin/env python3
"""Smoke-test a running vLLM OpenAI-compatible server."""

from __future__ import annotations

import argparse
import os

from vllm_skill_common import http_json, print_json


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000", help="Server base URL.")
    parser.add_argument("--model", default=None, help="Model name for generation requests.")
    parser.add_argument("--api-key", default=os.environ.get("VLLM_API_KEY"), help="Optional bearer key.")
    parser.add_argument("--list-models", action="store_true", help="Call /v1/models.")
    parser.add_argument("--chat", action="store_true", help="Call /v1/chat/completions.")
    parser.add_argument("--completion", action="store_true", help="Call /v1/completions.")
    parser.add_argument("--embedding", action="store_true", help="Call /v1/embeddings.")
    parser.add_argument("--prompt", default="Say hello in one short sentence.", help="Prompt text.")
    parser.add_argument("--max-tokens", type=int, default=16, help="Max generated tokens.")
    parser.add_argument("--json", action="store_true", help="Print JSON.")
    args = parser.parse_args()
    headers = {}
    if args.api_key:
        headers["Authorization"] = f"Bearer {args.api_key}"
    base = args.base_url.rstrip("/")
    results = {"base_url": base, "checks": []}
    health = http_json(f"{base}/health", headers=headers)
    results["checks"].append({"name": "health", **health})
    if args.list_models or not any([args.chat, args.completion, args.embedding]):
        results["checks"].append(
            {"name": "models", **http_json(f"{base}/v1/models", headers=headers)}
        )
    if args.chat:
        if not args.model:
            raise SystemExit("--model is required for --chat")
        payload = {
            "model": args.model,
            "messages": [{"role": "user", "content": args.prompt}],
            "temperature": 0,
            "max_tokens": args.max_tokens,
        }
        results["checks"].append(
            {
                "name": "chat",
                **http_json(f"{base}/v1/chat/completions", "POST", payload, headers=headers),
            }
        )
    if args.completion:
        if not args.model:
            raise SystemExit("--model is required for --completion")
        payload = {
            "model": args.model,
            "prompt": args.prompt,
            "temperature": 0,
            "max_tokens": args.max_tokens,
        }
        results["checks"].append(
            {
                "name": "completion",
                **http_json(f"{base}/v1/completions", "POST", payload, headers=headers),
            }
        )
    if args.embedding:
        if not args.model:
            raise SystemExit("--model is required for --embedding")
        payload = {"model": args.model, "input": [args.prompt]}
        results["checks"].append(
            {
                "name": "embedding",
                **http_json(f"{base}/v1/embeddings", "POST", payload, headers=headers),
            }
        )
    results["ok"] = all(check.get("ok") for check in results["checks"])
    if args.json:
        print_json(results)
    else:
        for check in results["checks"]:
            print(f"{check['name']}: {'ok' if check.get('ok') else 'fail'} {check.get('status')}")
    if not results["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
