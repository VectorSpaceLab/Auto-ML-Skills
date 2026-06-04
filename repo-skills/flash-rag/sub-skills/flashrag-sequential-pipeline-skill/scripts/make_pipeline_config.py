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
    parser.add_argument("--metrics", nargs="+", default=["em", "f1", "acc", "retrieval_recall"])
    parser.add_argument("--sample-num", type=int, default=3)
    parser.add_argument("--retrieval-topk", type=int, default=2)
    args = parser.parse_args()

    lines = [
        f"data_dir: {scalar(args.data_dir)}",
        f"dataset_name: {scalar(args.dataset_name)}",
        f"split: {list_value([args.split])}",
        f"save_dir: {scalar(args.save_dir)}",
        "save_note: pipeline",
        "gpu_id: null",
        "disable_save: false",
        "framework: openai",
        "generator_model: gpt-3.5-turbo",
        "generator_model_path: null",
        "generator_max_input_len: 1024",
        "generator_batch_size: 4",
        "generation_params:",
        "  max_tokens: 32",
        "retrieval_method: bm25",
        "bm25_backend: bm25s",
        "corpus_path: null",
        "index_path: null",
        f"retrieval_topk: {args.retrieval_topk}",
        "retrieval_batch_size: 32",
        "save_retrieval_cache: false",
        "use_retrieval_cache: false",
        "retrieval_cache_path: null",
        "use_reranker: false",
        "use_multi_retriever: false",
        "silent_retrieval: true",
        "use_fid: false",
        "refiner_name: null",
        "save_intermediate_data: true",
        "save_metric_score: true",
        f"metrics: {list_value(args.metrics)}",
        "metric_setting:",
        "  retrieval_recall_topk: 1",
        "  tokenizer_name: gpt-4",
        f"test_sample_num: {scalar(args.sample_num)}",
        "random_sample: false",
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
