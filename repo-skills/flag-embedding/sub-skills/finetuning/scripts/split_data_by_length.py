#!/usr/bin/env python3
"""Split FlagEmbedding fine-tune JSONL into approximate length buckets safely."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable, Iterable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-path", required=True, help="Input JSONL file or directory of JSONL files.")
    parser.add_argument("--output-dir", required=True, help="Directory for split JSONL outputs.")
    parser.add_argument("--length-list", nargs="+", type=int, default=[0, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000])
    parser.add_argument("--length-mode", choices=("chars", "whitespace-tokens", "hf-tokenizer"), default="chars")
    parser.add_argument("--model-name-or-path", default="BAAI/bge-m3", help="Tokenizer name/path for --length-mode hf-tokenizer.")
    parser.add_argument("--cache-dir", help="Tokenizer cache directory for --length-mode hf-tokenizer.")
    parser.add_argument("--log-name", default=".split_log", help="JSONL split log filename inside output dir.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing bucket files.")
    parser.add_argument("--allow-tokenizer-download", action="store_true", help="Acknowledge that hf-tokenizer mode may download tokenizer files.")
    parser.add_argument("--keep-empty-buckets", action="store_true", help="Create empty files for buckets with no records.")
    return parser.parse_args()


def input_files(path: Path) -> list[Path]:
    if not path.exists():
        raise FileNotFoundError(path)
    if path.is_dir():
        return sorted(child for child in path.rglob("*.jsonl") if child.is_file())
    return [path]


def ranges_from_bounds(bounds: Iterable[int]) -> list[tuple[int, float]]:
    unique_bounds = sorted(set(bounds))
    if not unique_bounds or unique_bounds[0] < 0:
        raise ValueError("length-list must contain non-negative integers")
    ranges: list[tuple[int, float]] = []
    for index, left in enumerate(unique_bounds):
        right = unique_bounds[index + 1] if index + 1 < len(unique_bounds) else math.inf
        if left >= right:
            raise ValueError("length-list must be strictly increasing after duplicates are removed")
        ranges.append((left, right))
    return ranges


def collect_texts(record: dict[str, Any]) -> list[str]:
    texts: list[str] = []
    query = record.get("query")
    if isinstance(query, str):
        texts.append(query)
    for field in ("pos", "neg"):
        value = record.get(field)
        if isinstance(value, list):
            texts.extend(item for item in value if isinstance(item, str))
    return texts


def chars_length(record: dict[str, Any]) -> int:
    texts = collect_texts(record)
    return max((len(text) for text in texts), default=0)


def whitespace_length(record: dict[str, Any]) -> int:
    texts = collect_texts(record)
    return max((len(text.split()) for text in texts), default=0)


def tokenizer_length_fn(model_name_or_path: str, cache_dir: str | None, allow_download: bool) -> Callable[[dict[str, Any]], int]:
    if not allow_download:
        raise RuntimeError("hf-tokenizer mode may download tokenizer files; rerun with --allow-tokenizer-download after approval")
    print("warning: hf-tokenizer mode may download tokenizer files via transformers", file=sys.stderr)
    try:
        from transformers import AutoTokenizer  # type: ignore
    except ImportError as exc:
        raise RuntimeError("transformers is required for --length-mode hf-tokenizer") from exc
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, cache_dir=cache_dir)

    def length(record: dict[str, Any]) -> int:
        texts = collect_texts(record)
        return max((len(tokenizer(text, add_special_tokens=True)["input_ids"]) for text in texts), default=0)

    return length


def bucket_label(left: int, right: float) -> str:
    right_label = "inf" if math.isinf(right) else str(int(right))
    return f"len-{left}-{right_label}"


def choose_bucket(length: int, ranges: list[tuple[int, float]]) -> tuple[int, float]:
    for left, right in ranges:
        if left <= length < right:
            return left, right
    return ranges[-1]


def read_records(path: Path) -> list[tuple[int, dict[str, Any]]]:
    records: list[tuple[int, dict[str, Any]]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                record = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: malformed JSON: {exc.msg}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"{path}:{line_number}: record must be a JSON object")
            records.append((line_number, record))
    return records


def split_file(path: Path, output_dir: Path, ranges: list[tuple[int, float]], length_fn: Callable[[dict[str, Any]], int], overwrite: bool, keep_empty: bool) -> dict[str, Any]:
    records = read_records(path)
    buckets: dict[str, list[dict[str, Any]]] = {bucket_label(left, right): [] for left, right in ranges}
    lengths: list[int] = []

    for _line_number, record in records:
        length = length_fn(record)
        lengths.append(length)
        label = bucket_label(*choose_bucket(length, ranges))
        buckets[label].append(record)

    written: dict[str, int] = {}
    stem = path.stem
    for label, items in buckets.items():
        output_path = output_dir / f"{stem}_{label}.jsonl"
        if output_path.exists() and not overwrite:
            written[str(output_path.name)] = -1
            continue
        if not items and not keep_empty:
            written[str(output_path.name)] = 0
            continue
        with output_path.open("w", encoding="utf-8") as handle:
            for item in items:
                handle.write(json.dumps(item, ensure_ascii=False) + "\n")
        written[str(output_path.name)] = len(items)

    return {
        "file_name": path.name,
        "records": len(records),
        "max_length": max(lengths) if lengths else 0,
        "avg_length": (sum(lengths) / len(lengths)) if lengths else 0,
        "buckets": {label: len(items) for label, items in buckets.items()},
        "written": written,
    }


def main() -> int:
    args = parse_args()
    try:
        ranges = ranges_from_bounds(args.length_list)
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        files = input_files(Path(args.input_path))
        if args.length_mode == "chars":
            length_fn = chars_length
        elif args.length_mode == "whitespace-tokens":
            length_fn = whitespace_length
        else:
            length_fn = tokenizer_length_fn(args.model_name_or_path, args.cache_dir, args.allow_tokenizer_download)

        logs = []
        for path in files:
            logs.append(split_file(path, output_dir, ranges, length_fn, args.overwrite, args.keep_empty_buckets))
        log_path = output_dir / args.log_name
        with log_path.open("a", encoding="utf-8") as handle:
            for item in logs:
                handle.write(json.dumps(item, ensure_ascii=False) + "\n")
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"OK: split {len(logs)} file(s) into {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
