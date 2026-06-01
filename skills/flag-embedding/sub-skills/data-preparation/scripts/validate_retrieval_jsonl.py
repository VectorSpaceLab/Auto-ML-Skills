#!/usr/bin/env python3
"""Validate FlagEmbedding retrieval training JSONL.

Examples:
    python scripts/validate_retrieval_jsonl.py --input train.jsonl --mode train
    python scripts/validate_retrieval_jsonl.py --input train_scored.jsonl --mode train --require-scores
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate_text_list(row: dict, key: str, path: Path, lineno: int) -> list[str]:
    value = row.get(key)
    if not isinstance(value, list) or not value:
        raise SystemExit(f"{path}:{lineno}: {key!r} must be a non-empty list")
    bad = [idx for idx, item in enumerate(value) if not isinstance(item, str) or not item]
    if bad:
        raise SystemExit(f"{path}:{lineno}: {key!r} contains non-string/empty items at {bad[:5]}")
    return value


def validate_score_list(row: dict, score_key: str, text_key: str, path: Path, lineno: int) -> None:
    scores = row.get(score_key)
    texts = row.get(text_key)
    if not isinstance(scores, list):
        raise SystemExit(f"{path}:{lineno}: {score_key!r} must be a list")
    if len(scores) != len(texts):
        raise SystemExit(f"{path}:{lineno}: {score_key!r} length {len(scores)} != {text_key!r} length {len(texts)}")
    for idx, score in enumerate(scores):
        if not isinstance(score, (int, float)):
            raise SystemExit(f"{path}:{lineno}: {score_key!r}[{idx}] must be numeric")


def validate_file(path: Path, require_scores: bool) -> tuple[int, int, int]:
    rows = positives = negatives = 0
    with path.open("r", encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise SystemExit(f"{path}:{lineno}: row must be a JSON object")
            if not isinstance(row.get("query"), str) or not row["query"]:
                raise SystemExit(f"{path}:{lineno}: 'query' must be a non-empty string")
            pos = validate_text_list(row, "pos", path, lineno)
            neg = validate_text_list(row, "neg", path, lineno)
            if require_scores or "pos_scores" in row or "neg_scores" in row:
                validate_score_list(row, "pos_scores", "pos", path, lineno)
                validate_score_list(row, "neg_scores", "neg", path, lineno)
            rows += 1
            positives += len(pos)
            negatives += len(neg)
    return rows, positives, negatives


def iter_inputs(input_path: Path) -> list[Path]:
    if input_path.is_dir():
        return sorted(input_path.glob("*.jsonl"))
    return [input_path]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="JSONL file or directory of JSONL files.")
    parser.add_argument("--mode", choices=["train"], default="train")
    parser.add_argument("--require-scores", action="store_true")
    args = parser.parse_args()

    paths = iter_inputs(Path(args.input))
    if not paths:
        raise SystemExit(f"No JSONL files found at {args.input}")
    total_rows = total_pos = total_neg = 0
    for path in paths:
        rows, pos, neg = validate_file(path, args.require_scores)
        print(f"OK {path}: rows={rows} pos={pos} neg={neg}")
        total_rows += rows
        total_pos += pos
        total_neg += neg
    print(f"TOTAL rows={total_rows} pos={total_pos} neg={total_neg}")


if __name__ == "__main__":
    main()
