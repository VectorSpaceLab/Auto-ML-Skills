#!/usr/bin/env python3
"""Validate a simple FlagEmbedding custom evaluation dataset layout.

Example:
    python scripts/check_eval_dataset.py --dataset-dir ./eval_data --splits test dev
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}") from exc
            if not isinstance(value, dict):
                raise SystemExit(f"{path}:{lineno}: row must be a JSON object")
            rows.append(value)
    return rows


def validate_one(dataset_dir: Path, splits: list[str]) -> None:
    corpus_path = dataset_dir / "corpus.jsonl"
    if not corpus_path.exists():
        raise SystemExit(f"Missing {corpus_path}")
    corpus = read_jsonl(corpus_path)
    doc_ids = {str(row.get("id")) for row in corpus if row.get("id") is not None}
    if not doc_ids:
        print(f"Warning: no 'id' fields found in {corpus_path}")

    for split in splits:
        queries_path = dataset_dir / f"{split}_queries.jsonl"
        qrels_path = dataset_dir / f"{split}_qrels.jsonl"
        if not queries_path.exists():
            raise SystemExit(f"Missing {queries_path}")
        if not qrels_path.exists():
            raise SystemExit(f"Missing {qrels_path}")

        queries = read_jsonl(queries_path)
        qrels = read_jsonl(qrels_path)
        query_ids = {str(row.get("id")) for row in queries if row.get("id") is not None}
        if not query_ids:
            print(f"Warning: no 'id' fields found in {queries_path}")

        missing_qids = []
        missing_docids = []
        for row in qrels:
            qid = row.get("qid", row.get("query_id"))
            docid = row.get("docid", row.get("doc_id", row.get("corpus_id")))
            if query_ids and str(qid) not in query_ids:
                missing_qids.append(qid)
            if doc_ids and str(docid) not in doc_ids:
                missing_docids.append(docid)
        if missing_qids:
            print(f"Warning: {len(missing_qids)} qrels qids are absent from {queries_path}")
        if missing_docids:
            print(f"Warning: {len(missing_docids)} qrels docids are absent from {corpus_path}")

        print(f"OK {dataset_dir} split={split}: corpus={len(corpus)} queries={len(queries)} qrels={len(qrels)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", required=True)
    parser.add_argument("--splits", nargs="+", default=["test"])
    parser.add_argument("--children", action="store_true", help="Validate each child directory as a dataset.")
    args = parser.parse_args()

    root = Path(args.dataset_dir)
    if args.children:
        dirs = [path for path in sorted(root.iterdir()) if path.is_dir()]
        if not dirs:
            raise SystemExit(f"No child directories found under {root}")
    else:
        dirs = [root]
    for dataset_dir in dirs:
        validate_one(dataset_dir, args.splits)


if __name__ == "__main__":
    main()
