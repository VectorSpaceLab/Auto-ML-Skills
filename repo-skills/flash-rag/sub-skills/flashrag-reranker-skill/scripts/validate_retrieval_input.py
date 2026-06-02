#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    docs = payload.get("docs") or payload.get("retrieval_result") or []
    errors = []
    if not isinstance(docs, list) or not docs:
        errors.append("no docs/retrieval_result list")
    else:
        print(f"docs: {len(docs)}")
        print("first_keys: " + ",".join(sorted(docs[0].keys())))
        if "contents" not in docs[0]:
            errors.append("first doc missing contents")
    print(f"valid: {str(not errors).lower()}")
    for error in errors:
        print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
