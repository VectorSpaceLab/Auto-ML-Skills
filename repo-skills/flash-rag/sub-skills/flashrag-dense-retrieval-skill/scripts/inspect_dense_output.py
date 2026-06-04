#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index-path", type=Path, required=True)
    parser.add_argument("--search-output", type=Path, required=True)
    args = parser.parse_args()
    errors = []
    print(f"index_path: {args.index_path.resolve()}")
    if not args.index_path.exists():
        errors.append("index path missing")
    if not args.search_output.exists():
        errors.append("search output missing")
    else:
        payload = json.loads(args.search_output.read_text(encoding="utf-8"))
        docs = payload.get("docs", [])
        print(f"docs: {len(docs)}")
        if docs:
            print("first_doc_id: " + str(docs[0].get("id")))
        else:
            errors.append("no retrieved docs")
    print(f"valid: {str(not errors).lower()}")
    for error in errors:
        print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
