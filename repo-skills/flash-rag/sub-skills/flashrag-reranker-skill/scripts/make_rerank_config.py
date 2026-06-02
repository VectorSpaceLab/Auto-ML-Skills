#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base-config", type=Path, required=True)
    parser.add_argument("--rerank-model-name", required=True)
    parser.add_argument("--rerank-model-path", required=True)
    parser.add_argument("--rerank-topk", type=int, default=5)
    parser.add_argument("--rerank-max-length", type=int, default=512)
    args = parser.parse_args()
    text = args.base_config.read_text(encoding="utf-8")
    additions = [
        "use_reranker: true",
        f"rerank_model_name: {args.rerank_model_name}",
        f"rerank_model_path: {args.rerank_model_path}",
        f"rerank_topk: {args.rerank_topk}",
        f"rerank_max_length: {args.rerank_max_length}",
        "rerank_batch_size: 16",
        "rerank_use_fp16: true",
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text.rstrip() + "\n" + "\n".join(additions) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
