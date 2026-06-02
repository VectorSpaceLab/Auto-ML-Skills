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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--generator-model", default="gpt-3.5-turbo")
    parser.add_argument("--max-input-len", type=int, default=512)
    parser.add_argument("--save-dir", default="./work/fr_prompt_outputs")
    args = parser.parse_args()

    lines = [
        "data_dir: dataset",
        "dataset_name: nq",
        "split: [test]",
        f"save_dir: {scalar(args.save_dir)}",
        "save_note: prompt",
        "gpu_id: null",
        "disable_save: true",
        "framework: openai",
        f"generator_model: {scalar(args.generator_model)}",
        "generator_model_path: null",
        f"generator_max_input_len: {args.max_input_len}",
        "generator_batch_size: 1",
        "generation_params:",
        "  max_tokens: 32",
        "retrieval_method: bm25",
        "corpus_path: null",
        "index_path: null",
        "retrieval_topk: 3",
        "save_retrieval_cache: false",
        "use_retrieval_cache: false",
        "retrieval_cache_path: null",
        "use_reranker: false",
        "use_multi_retriever: false",
        "use_fid: false",
        "refiner_name: lexical-offline",
        "refiner_model_path: null",
        "refiner_input_prompt_flag: false",
        "metrics: [em]",
        "metric_setting:",
        "  retrieval_recall_topk: 1",
        "  tokenizer_name: gpt-4",
        "save_intermediate_data: true",
        "save_metric_score: true",
        "test_sample_num: null",
        "random_sample: false",
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
