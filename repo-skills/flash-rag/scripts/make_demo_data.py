#!/usr/bin/env python3
"""Create tiny self-contained FlashRAG QA datasets and corpora.

Example:
  python scripts/make_demo_data.py --data-dir ./dataset --dataset-name tiny_qa --corpus ./corpus.jsonl
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


QA_ROWS = [
    {"id": "q1", "question": "What is the capital of France?", "golden_answers": ["Paris"]},
    {"id": "q2", "question": "Which field combines retrieval with generation?", "golden_answers": ["RAG"]},
]

CORPUS_ROWS = [
    {"id": "doc1", "title": "France", "contents": "France\nParis is the capital city of France."},
    {
        "id": "doc2",
        "title": "Retrieval augmented generation",
        "contents": "Retrieval augmented generation\nRAG combines retrieval with text generation.",
    },
]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", default="tiny_qa")
    parser.add_argument("--split", default="test")
    parser.add_argument("--corpus", type=Path, default=None)
    args = parser.parse_args()

    dataset_path = args.data_dir / args.dataset_name / f"{args.split}.jsonl"
    write_jsonl(dataset_path, QA_ROWS)
    corpus_path = args.corpus or (args.data_dir / "corpus.jsonl")
    write_jsonl(corpus_path, CORPUS_ROWS)
    print(f"data_dir: {args.data_dir.resolve()}")
    print(f"dataset_name: {args.dataset_name}")
    print(f"dataset_file: {dataset_path}")
    print(f"corpus: {corpus_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
