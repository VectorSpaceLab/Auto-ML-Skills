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
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--split", default="test")
    parser.add_argument("--save-dir", required=True)
    parser.add_argument("--pipeline", choices=["selfrag", "flare", "selfask", "ircot", "rqrag", "rqrAG"], default="selfask")
    parser.add_argument("--sample-num", type=int, default=3)
    parser.add_argument("--retrieval-topk", type=int, default=2)
    parser.add_argument("--max-iter", type=int, default=2)
    args = parser.parse_args()
    cfg = {
        "data_dir": args.data_dir,
        "dataset_name": args.dataset_name,
        "split": [args.split],
        "save_dir": args.save_dir,
        "save_note": f"active-{args.pipeline.lower()}",
        "disable_save": False,
        "gpu_id": None,
        "pipeline_name": args.pipeline.lower(),
        "framework": "openai",
        "generator_model": "gpt-3.5-turbo",
        "generator_model_path": None,
        "generation_params": {"max_tokens": 64},
        "retrieval_method": "bm25",
        "bm25_backend": "bm25s",
        "corpus_path": None,
        "index_path": None,
        "retrieval_topk": args.retrieval_topk,
        "retrieval_batch_size": 32,
        "retrieval_use_fp16": False,
        "use_reranker": False,
        "use_multi_retriever": False,
        "use_retrieval_cache": False,
        "save_retrieval_cache": False,
        "retrieval_cache_path": None,
        "use_fid": False,
        "refiner_name": None,
        "max_iter": args.max_iter,
        "save_intermediate_data": True,
        "save_metric_score": True,
        "metrics": ["em", "f1", "acc", "retrieval_recall"],
        "metric_setting": {"retrieval_recall_topk": 1, "tokenizer_name": "gpt-4"},
        "test_sample_num": args.sample_num,
        "random_sample": False,
    }
    write_yaml(args.output, cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
