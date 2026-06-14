#!/usr/bin/env python3
"""Validate a FlagEmbedding custom evaluation dataset layout.

The script checks JSONL parseability, required split files, basic ids, and qrel
references. It performs no downloads and does not import FlagEmbedding.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DOC_ID_KEYS = ("id", "_id", "docid", "doc_id", "corpus-id", "corpus_id")
QUERY_ID_KEYS = ("id", "_id", "qid", "query-id", "query_id")
TEXT_KEYS = ("text", "contents", "body")
QREL_QUERY_KEYS = ("query-id", "query_id", "qid", "id")
QREL_DOC_KEYS = ("corpus-id", "corpus_id", "docid", "doc_id", "pid")


def first_key(row: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        if key in row:
            return row[key]
    return None


def read_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, raw in enumerate(fh, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{path}: line {line_no}: invalid JSON: {exc.msg}")
                continue
            if not isinstance(row, dict):
                errors.append(f"{path}: line {line_no}: row must be a JSON object")
                continue
            rows.append(row)
    if not rows:
        errors.append(f"{path}: file has no JSON rows")
    return rows, errors


def dataset_dirs(root: Path, dataset_names: list[str] | None) -> list[Path]:
    if dataset_names:
        return [root / name for name in dataset_names]
    if (root / "corpus.jsonl").exists():
        return [root]
    children = [child for child in root.iterdir() if child.is_dir()]
    return children or [root]


def validate_dataset(path: Path, splits: list[str], max_missing_refs: int) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"{path}: dataset directory does not exist"]
    if not path.is_dir():
        return [f"{path}: expected directory"]

    corpus_path = path / "corpus.jsonl"
    if not corpus_path.exists():
        return [f"{path}: missing corpus.jsonl"]

    corpus_rows, row_errors = read_jsonl(corpus_path)
    errors.extend(row_errors)
    doc_ids: set[str] = set()
    for idx, row in enumerate(corpus_rows, start=1):
        doc_id = first_key(row, DOC_ID_KEYS)
        text = first_key(row, TEXT_KEYS)
        if doc_id is None:
            errors.append(f"{corpus_path}: row {idx}: missing document id key")
        else:
            doc_ids.add(str(doc_id))
        if text is None or not isinstance(text, str):
            errors.append(f"{corpus_path}: row {idx}: missing text string")

    for split in splits:
        queries_path = path / f"{split}_queries.jsonl"
        qrels_path = path / f"{split}_qrels.jsonl"
        if not queries_path.exists():
            errors.append(f"{path}: missing {split}_queries.jsonl")
            continue
        if not qrels_path.exists():
            errors.append(f"{path}: missing {split}_qrels.jsonl")
            continue

        query_rows, row_errors = read_jsonl(queries_path)
        errors.extend(row_errors)
        query_ids: set[str] = set()
        for idx, row in enumerate(query_rows, start=1):
            query_id = first_key(row, QUERY_ID_KEYS)
            text = first_key(row, TEXT_KEYS)
            if query_id is None:
                errors.append(f"{queries_path}: row {idx}: missing query id key")
            else:
                query_ids.add(str(query_id))
            if text is None or not isinstance(text, str):
                errors.append(f"{queries_path}: row {idx}: missing text string")

        qrel_rows, row_errors = read_jsonl(qrels_path)
        errors.extend(row_errors)
        missing_refs = 0
        for idx, row in enumerate(qrel_rows, start=1):
            query_id = first_key(row, QREL_QUERY_KEYS)
            doc_id = first_key(row, QREL_DOC_KEYS)
            if query_id is None:
                errors.append(f"{qrels_path}: row {idx}: missing query id reference")
            elif str(query_id) not in query_ids and missing_refs < max_missing_refs:
                errors.append(f"{qrels_path}: row {idx}: query id {query_id!r} not found in {queries_path.name}")
                missing_refs += 1
            if doc_id is None:
                errors.append(f"{qrels_path}: row {idx}: missing document id reference")
            elif str(doc_id) not in doc_ids and missing_refs < max_missing_refs:
                errors.append(f"{qrels_path}: row {idx}: document id {doc_id!r} not found in corpus.jsonl")
                missing_refs += 1

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_dir")
    parser.add_argument("--dataset-names", nargs="+", help="Optional dataset subdirectories to validate.")
    parser.add_argument("--splits", nargs="+", default=["test"])
    parser.add_argument("--max-missing-refs", type=int, default=20)
    args = parser.parse_args()

    root = Path(args.dataset_dir)
    all_errors: list[str] = []
    checked: list[str] = []
    if not root.exists():
        all_errors.append(f"{root}: directory does not exist")
    else:
        for path in dataset_dirs(root, args.dataset_names):
            checked.append(str(path))
            all_errors.extend(validate_dataset(path, args.splits, args.max_missing_refs))

    report = {"ok": not all_errors, "checked": checked, "splits": args.splits, "errors": all_errors}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
