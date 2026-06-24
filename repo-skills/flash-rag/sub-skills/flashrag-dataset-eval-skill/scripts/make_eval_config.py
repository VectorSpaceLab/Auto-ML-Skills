#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any


def scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if text == "" or any(ch in text for ch in ":#{}[],&*?|-<>=!%@`\"'"):
        return repr(text)
    return text


def list_value(values: list[str]) -> str:
    return "[" + ", ".join(scalar(v) for v in values) + "]"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--split", default="test")
    parser.add_argument("--save-dir", required=True)
    parser.add_argument("--metrics", nargs="+", default=["em", "f1", "acc"])
    parser.add_argument("--test-sample-num", type=int, default=None)
    args = parser.parse_args()
    lines = [
        f"data_dir: {scalar(args.data_dir)}",
        f"dataset_name: {scalar(args.dataset_name)}",
        f"split: {list_value([args.split])}",
        f"save_dir: {scalar(args.save_dir)}",
        "save_note: eval",
        "save_intermediate_data: true",
        "save_metric_score: true",
        f"metrics: {list_value(args.metrics)}",
        "metric_setting:",
        "  retrieval_recall_topk: 1",
        "  tokenizer_name: gpt-4",
        "gpu_id: null",
        "disable_save: false",
        "test_sample_num: " + scalar(args.test_sample_num),
        "random_sample: false",
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
