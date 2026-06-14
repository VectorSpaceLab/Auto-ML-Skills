#!/usr/bin/env python3
"""Validate common SGLang retrieval/ranking endpoint payloads."""

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate embeddings/rerank/score/classify payload shape.")
    parser.add_argument("json_file", nargs="?")
    parser.add_argument("--endpoint", choices=["embeddings", "rerank", "score", "classify"], default="embeddings")
    args = parser.parse_args()
    if not args.json_file:
        print("Provide a JSON payload file; --help is lightweight.")
        return 0
    data = json.load(open(args.json_file, encoding="utf-8"))
    issues = []
    if args.endpoint == "embeddings":
        if "input" not in data and "text" not in data:
            issues.append("embeddings payload should include input or text")
    elif args.endpoint == "rerank":
        if "query" not in data:
            issues.append("rerank payload should include query")
        if "documents" not in data and "texts" not in data:
            issues.append("rerank payload should include documents or texts")
    elif args.endpoint in {"score", "classify"}:
        if not any(k in data for k in ["input", "text", "query"]):
            issues.append(f"{args.endpoint} payload should include input/text/query")
    print(json.dumps({"ok": not issues, "issues": issues}, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
