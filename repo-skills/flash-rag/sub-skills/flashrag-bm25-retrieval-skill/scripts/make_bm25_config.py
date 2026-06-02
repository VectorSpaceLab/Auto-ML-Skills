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
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--index-path", type=Path, required=True)
    parser.add_argument("--save-dir", type=Path, required=True)
    parser.add_argument("--topk", type=int, default=3)
    parser.add_argument("--dataset-name", default="nq")
    parser.add_argument("--data-dir", default="dataset")
    parser.add_argument("--split", default="test")
    parser.add_argument("--metrics", nargs="+", default=["retrieval_recall"])
    args = parser.parse_args()

    lines = [
        f"data_dir: {scalar(args.data_dir)}",
        f"dataset_name: {scalar(args.dataset_name)}",
        f"split: {list_value([args.split])}",
        f"save_dir: {scalar(str(args.save_dir))}",
        "save_note: bm25",
        "gpu_id: null",
        "disable_save: true",
        "retrieval_method: bm25",
        "bm25_backend: bm25s",
        f"corpus_path: {scalar(str(args.corpus.resolve()))}",
        f"index_path: {scalar(str(args.index_path.resolve()))}",
        f"retrieval_topk: {args.topk}",
        "retrieval_batch_size: 32",
        "save_retrieval_cache: false",
        "use_retrieval_cache: false",
        "retrieval_cache_path: null",
        "use_reranker: false",
        "use_multi_retriever: false",
        "silent_retrieval: true",
        "framework: openai",
        "generator_model: gpt-3.5-turbo",
        "generator_model_path: null",
        "generator_max_input_len: 1024",
        f"metrics: {list_value(args.metrics)}",
        "metric_setting:",
        f"  retrieval_recall_topk: {args.topk}",
        "  tokenizer_name: gpt-4",
        "save_intermediate_data: true",
        "save_metric_score: true",
        "test_sample_num: null",
        "random_sample: false",
        "refiner_name: null",
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
