#!/usr/bin/env python3
"""Validate FlagEmbedding fine-tuning JSONL without ML dependencies."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

ALLOWED_MODES = ("embedder", "reranker", "auto")
KNOWN_ICL_TYPES = {
    "normal",
    "symmetric_class",
    "symmetric_clustering",
    "classification",
    "clustering",
    "retrieval",
    "sts",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", nargs="*", help="JSONL file(s) or directorie(s) to validate.")
    parser.add_argument("--candidate-pool", help="Validate a hard-negative candidate pool JSONL with a text field.")
    parser.add_argument("--mode", choices=ALLOWED_MODES, default="auto", help="Training target mode for messages.")
    parser.add_argument("--check-scores", action="store_true", help="Require and validate pos_scores/neg_scores alignment.")
    parser.add_argument("--require-negatives", action="store_true", help="Require every record to have at least one negative.")
    parser.add_argument("--require-prompt", action="store_true", help="Require prompt on every record, useful for prompt-based rerankers.")
    parser.add_argument("--require-icl-type", action="store_true", help="Require type on every record, useful for ICL embedder data.")
    parser.add_argument("--warn-unknown-icl-type", action="store_true", help="Warn when type is outside common observed values.")
    parser.add_argument("--max-errors", type=int, default=50, help="Stop after this many errors per run.")
    return parser.parse_args()


def iter_jsonl_files(paths: Iterable[str]) -> list[Path]:
    files: list[Path] = []
    for raw_path in paths:
        path = Path(raw_path)
        if not path.exists():
            raise FileNotFoundError(f"path does not exist: {path}")
        if path.is_dir():
            files.extend(sorted(child for child in path.rglob("*.jsonl") if child.is_file()))
        else:
            files.append(path)
    return files


def is_non_empty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_text_list(value: Any, field: str, line_label: str, errors: list[str], require_non_empty: bool) -> int:
    if not isinstance(value, list):
        errors.append(f"{line_label}: {field} must be a list of strings")
        return 0
    if require_non_empty and not value:
        errors.append(f"{line_label}: {field} must not be empty")
    for index, item in enumerate(value):
        if not is_non_empty_str(item):
            errors.append(f"{line_label}: {field}[{index}] must be a non-empty string")
    return len(value)


def validate_scores(value: Any, expected_len: int, field: str, line_label: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{line_label}: {field} must be a list of numbers")
        return
    if len(value) != expected_len:
        errors.append(f"{line_label}: {field} length {len(value)} does not match expected {expected_len}")
    for index, item in enumerate(value):
        if not isinstance(item, (int, float)) or isinstance(item, bool):
            errors.append(f"{line_label}: {field}[{index}] must be a numeric JSON value")


def validate_train_record(record: Any, line_label: str, args: argparse.Namespace, errors: list[str], warnings: list[str]) -> None:
    if not isinstance(record, dict):
        errors.append(f"{line_label}: record must be a JSON object")
        return

    if not is_non_empty_str(record.get("query")):
        errors.append(f"{line_label}: query must be a non-empty string")

    pos_len = validate_text_list(record.get("pos"), "pos", line_label, errors, require_non_empty=True)
    neg_len = validate_text_list(record.get("neg"), "neg", line_label, errors, require_non_empty=args.require_negatives)

    if args.require_prompt and not is_non_empty_str(record.get("prompt")):
        errors.append(f"{line_label}: prompt is required and must be a non-empty string")

    record_type = record.get("type")
    if args.require_icl_type and not is_non_empty_str(record_type):
        errors.append(f"{line_label}: type is required for ICL data")
    elif record_type is not None:
        if not is_non_empty_str(record_type):
            errors.append(f"{line_label}: type must be a non-empty string when present")
        elif args.warn_unknown_icl_type and record_type not in KNOWN_ICL_TYPES:
            warnings.append(f"{line_label}: uncommon type value {record_type!r}; verify ICL formatting")

    if args.check_scores:
        if "pos_scores" not in record:
            errors.append(f"{line_label}: pos_scores missing while --check-scores is enabled")
        else:
            validate_scores(record["pos_scores"], pos_len, "pos_scores", line_label, errors)
        if "neg_scores" not in record:
            errors.append(f"{line_label}: neg_scores missing while --check-scores is enabled")
        else:
            validate_scores(record["neg_scores"], neg_len, "neg_scores", line_label, errors)
    else:
        if "pos_scores" in record:
            validate_scores(record["pos_scores"], pos_len, "pos_scores", line_label, errors)
        if "neg_scores" in record:
            validate_scores(record["neg_scores"], neg_len, "neg_scores", line_label, errors)

    query = record.get("query")
    positives = record.get("pos") if isinstance(record.get("pos"), list) else []
    negatives = record.get("neg") if isinstance(record.get("neg"), list) else []
    positive_set = {item for item in positives if isinstance(item, str)}
    for index, negative in enumerate(negatives):
        if isinstance(negative, str) and negative in positive_set:
            warnings.append(f"{line_label}: neg[{index}] duplicates a positive passage")
        if isinstance(negative, str) and isinstance(query, str) and negative == query:
            warnings.append(f"{line_label}: neg[{index}] duplicates the query text")


def validate_candidate_pool(path: Path, max_errors: int) -> tuple[int, list[str], list[str]]:
    count = 0
    errors: list[str] = []
    warnings: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped:
                warnings.append(f"{path}:{line_number}: blank line ignored")
                continue
            try:
                record = json.loads(stripped)
            except json.JSONDecodeError as exc:
                errors.append(f"{path}:{line_number}: malformed JSON: {exc.msg}")
                if len(errors) >= max_errors:
                    break
                continue
            if not isinstance(record, dict):
                errors.append(f"{path}:{line_number}: candidate record must be an object")
            elif not is_non_empty_str(record.get("text")):
                errors.append(f"{path}:{line_number}: candidate record needs non-empty text")
            count += 1
            if len(errors) >= max_errors:
                break
    return count, errors, warnings


def validate_file(path: Path, args: argparse.Namespace) -> tuple[int, list[str], list[str]]:
    count = 0
    errors: list[str] = []
    warnings: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped:
                warnings.append(f"{path}:{line_number}: blank line ignored")
                continue
            try:
                record = json.loads(stripped)
            except json.JSONDecodeError as exc:
                errors.append(f"{path}:{line_number}: malformed JSON: {exc.msg}")
                if len(errors) >= args.max_errors:
                    break
                continue
            validate_train_record(record, f"{path}:{line_number}", args, errors, warnings)
            count += 1
            if len(errors) >= args.max_errors:
                break
    return count, errors, warnings


def main() -> int:
    args = parse_args()
    if not args.input and not args.candidate_pool:
        print("error: provide --input and/or --candidate-pool", file=sys.stderr)
        return 2

    all_errors: list[str] = []
    all_warnings: list[str] = []
    total_records = 0
    total_files = 0

    try:
        if args.input:
            for path in iter_jsonl_files(args.input):
                total_files += 1
                count, errors, warnings = validate_file(path, args)
                total_records += count
                all_errors.extend(errors)
                all_warnings.extend(warnings)
        if args.candidate_pool:
            total_files += 1
            count, errors, warnings = validate_candidate_pool(Path(args.candidate_pool), args.max_errors)
            total_records += count
            all_errors.extend(errors)
            all_warnings.extend(warnings)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    for warning in all_warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in all_errors:
        print(f"error: {error}", file=sys.stderr)

    if all_errors:
        print(f"FAILED: {len(all_errors)} error(s), {len(all_warnings)} warning(s), {total_records} record(s), {total_files} file(s)")
        return 1

    print(f"OK: {total_records} record(s), {total_files} file(s), {len(all_warnings)} warning(s), mode={args.mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
