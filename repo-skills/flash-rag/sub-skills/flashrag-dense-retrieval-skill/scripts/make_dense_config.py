#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import write_yaml


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--index-path", type=Path, required=True)
    parser.add_argument("--retrieval-method", required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--save-dir", type=Path, required=True)
    parser.add_argument("--pooling-method", default="mean")
    parser.add_argument("--topk", type=int, default=5)
    args = parser.parse_args()
    cfg = {
        "data_dir": "dataset",
        "dataset_name": "nq",
        "split": ["test"],
        "save_dir": str(args.save_dir),
        "save_note": "dense",
        "disable_save": True,
        "gpu_id": None,
        "model2path": {args.retrieval_method: args.model_path},
        "model2pooling": {args.retrieval_method: args.pooling_method},
        "retrieval_method": args.retrieval_method,
        "corpus_path": str(args.corpus.resolve()),
        "index_path": str(args.index_path.resolve()),
        "retrieval_topk": args.topk,
        "retrieval_batch_size": 32,
        "retrieval_use_fp16": False,
        "retrieval_query_max_length": 128,
        "use_reranker": False,
        "framework": "openai",
        "generator_model": "gpt-3.5-turbo",
        "metrics": ["retrieval_recall"],
        "metric_setting": {"retrieval_recall_topk": args.topk},
        "save_intermediate_data": True,
        "save_metric_score": True,
        "refiner_name": None,
    }
    write_yaml(args.output, cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
