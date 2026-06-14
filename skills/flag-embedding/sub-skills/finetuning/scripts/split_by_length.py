#!/usr/bin/env python3
"""Split FlagEmbedding training JSONL rows into token-length buckets.

This script loads a tokenizer and can download it from Hugging Face.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


def read_rows(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, raw in enumerate(fh, start=1):
            if not raw.strip():
                continue
            row = json.loads(raw)
            if not isinstance(row, dict):
                raise ValueError(f"{path}: line {line_no}: expected JSON object")
            rows.append(row)
    return rows


def iter_input_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        return sorted(child for child in path.iterdir() if child.suffix == ".jsonl")
    raise FileNotFoundError(str(path))


def ranges(lengths: list[int]) -> list[tuple[int, float]]:
    values = sorted(lengths)
    if len(values) < 2:
        raise ValueError("--length_list must contain at least two values")
    out: list[tuple[int, float]] = []
    for idx, left in enumerate(values):
        right = values[idx + 1] if idx + 1 < len(values) else math.inf
        if left < 0 or right <= left:
            raise ValueError("length values must be non-negative and increasing")
        out.append((left, right))
    return out


def max_row_length(row: dict[str, Any], tokenizer: Any) -> int:
    texts = []
    query = row.get("query")
    if isinstance(query, str):
        texts.append(query)
    for key in ("pos", "neg"):
        value = row.get(key, [])
        if isinstance(value, list):
            texts.extend(item for item in value if isinstance(item, str))
    if not texts:
        return 0
    return max(len(tokenizer(text)["input_ids"]) for text in texts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input_path", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--model_name_or_path", default="BAAI/bge-m3")
    parser.add_argument("--cache_dir")
    parser.add_argument("--length_list", type=int, nargs="+", default=[0, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000])
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    try:
        from transformers import AutoTokenizer

        input_files = iter_input_files(Path(args.input_path))
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path, cache_dir=args.cache_dir)
        buckets = ranges(args.length_list)
        report = {"ok": True, "files": []}

        for input_file in input_files:
            rows = read_rows(input_file)
            bucket_rows: dict[str, list[dict[str, Any]]] = {}
            for row in rows:
                row_len = max_row_length(row, tokenizer)
                for left, right in buckets:
                    if left <= row_len < right:
                        key = f"len-{left}-{right}"
                        bucket_rows.setdefault(key, []).append(row)
                        break
            file_report = {"input": str(input_file), "rows": len(rows), "outputs": {}}
            stem = input_file.stem
            for key, selected in bucket_rows.items():
                if not selected:
                    continue
                output_path = output_dir / f"{stem}_{key}.jsonl"
                if output_path.exists() and not args.overwrite:
                    file_report["outputs"][str(output_path)] = "exists-skipped"
                    continue
                with output_path.open("w", encoding="utf-8") as fh:
                    for row in selected:
                        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                file_report["outputs"][str(output_path)] = len(selected)
            report["files"].append(file_report)

        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"}, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
