#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_INDEX_FILES = {
    "data.csc.index.npy",
    "indices.csc.index.npy",
    "indptr.csc.index.npy",
    "vocab.index.json",
    "stopwords.tokenizer.json",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index-dir", type=Path, required=True)
    parser.add_argument("--search-output", type=Path, required=True)
    args = parser.parse_args()

    errors: list[str] = []
    print(f"index_dir: {args.index_dir.resolve()}")
    if not args.index_dir.is_dir():
        errors.append("index_dir is missing")
        index_names: set[str] = set()
    else:
        index_names = {path.name for path in args.index_dir.iterdir()}
        for name in sorted(index_names):
            print(f"- {name}")
        missing = REQUIRED_INDEX_FILES - index_names
        if missing:
            errors.append(f"missing index files: {sorted(missing)}")

    if not args.search_output.is_file():
        errors.append("search_output is missing")
    else:
        payload = json.loads(args.search_output.read_text(encoding="utf-8"))
        results = payload.get("results", [])
        print(f"queries: {len(results)}")
        for idx, item in enumerate(results[:3]):
            docs = item.get("docs", [])
            print(f"query_{idx}_docs: {len(docs)}")
            if docs:
                print(f"query_{idx}_first_id: {docs[0].get('id')}")
                print(f"query_{idx}_first_preview: {str(docs[0].get('contents', ''))[:180].replace(chr(10), ' ')}")
        if not results or any(not item.get("docs") for item in results):
            errors.append("one or more queries returned no documents")

    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
