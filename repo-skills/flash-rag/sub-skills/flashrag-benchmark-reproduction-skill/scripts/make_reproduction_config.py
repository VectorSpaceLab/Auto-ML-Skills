#!/usr/bin/env python3
"""Emit a FlashRAG benchmark-style reproduction config skeleton."""

from __future__ import annotations

import argparse


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a FlashRAG reproduction YAML skeleton.")
    parser.add_argument("--generator-model", required=True)
    parser.add_argument("--retriever-model", required=True)
    parser.add_argument("--index-path", required=True)
    parser.add_argument("--corpus-path", required=True)
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--save-dir", default="flashrag_reproduction_outputs")
    parser.add_argument("--framework", choices=["vllm", "hf"], default="vllm")
    parser.add_argument("--test-sample-num", type=int, default=1000)
    args = parser.parse_args()
    print(
        f"""model2path:
  e5: {args.retriever_model}
  llama3-8B-instruct: {args.generator_model}
method2index:
  e5: {args.index_path}
corpus_path: {args.corpus_path}
data_dir: {args.data_dir}
save_dir: {args.save_dir}

retrieval_method: e5
retrieval_topk: 5
generator_model: llama3-8B-instruct
framework: {args.framework}
generation_params:
  do_sample: false
  max_tokens: 32
  temperature: 0.0
  top_p: 1.0
test_sample_num: {args.test_sample_num}
random_sample: false"""
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
