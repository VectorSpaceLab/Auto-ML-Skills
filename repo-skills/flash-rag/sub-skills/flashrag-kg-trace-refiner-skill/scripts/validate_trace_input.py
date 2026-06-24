#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    errors: list[str] = []
    rows = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    doc_count = 0
    for idx, row in enumerate(rows):
        if not str(row.get("question", "")).strip():
            errors.append(f"row {idx}: missing question")
        docs = row.get("retrieval_result")
        if not isinstance(docs, list) or not docs:
            errors.append(f"row {idx}: retrieval_result must be a non-empty list")
            continue
        for j, doc in enumerate(docs):
            doc_count += 1
            if not str(doc.get("contents", "")).strip():
                errors.append(f"row {idx} doc {j}: missing contents")
    print(f"records: {len(rows)}")
    print(f"retrieved_docs: {doc_count}")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
