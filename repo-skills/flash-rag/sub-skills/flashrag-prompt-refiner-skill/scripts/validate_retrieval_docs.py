#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from doc_utils import load_docs, validate_docs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs", type=Path, required=True)
    parser.add_argument("--result-index", type=int, default=0)
    parser.add_argument("--jsonl-limit", type=int, default=None)
    parser.add_argument("--max-errors", type=int, default=20)
    args = parser.parse_args()

    docs = load_docs(args.docs, result_index=args.result_index, jsonl_limit=args.jsonl_limit)
    errors = validate_docs(docs)[: args.max_errors]
    print(f"docs: {len(docs)}")
    if docs:
        print(f"first_id: {docs[0].get('id')}")
        print(f"first_preview: {str(docs[0].get('contents', ''))[:180].replace(chr(10), ' ')}")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
