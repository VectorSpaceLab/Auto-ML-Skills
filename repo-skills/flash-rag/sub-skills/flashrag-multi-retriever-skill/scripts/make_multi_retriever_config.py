#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import write_yaml


def parse_spec(spec: str) -> dict:
    parts = spec.split(":")
    if len(parts) != 4:
        raise ValueError("--retriever must be method:corpus_path:index_path:topk")
    method, corpus, index, topk = parts
    item = {"retrieval_method": method, "corpus_path": corpus, "index_path": index, "retrieval_topk": int(topk)}
    if method == "bm25":
        item["bm25_backend"] = "bm25s"
    return item


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--save-dir", required=True)
    parser.add_argument("--split", default="test")
    parser.add_argument("--merge-method", choices=["concat", "rrf", "rerank"], default="rrf")
    parser.add_argument("--topk", type=int, default=5)
    parser.add_argument("--retriever", action="append", required=True)
    args = parser.parse_args()
    cfg = {
        "data_dir": args.data_dir,
        "dataset_name": args.dataset_name,
        "split": [args.split],
        "save_dir": args.save_dir,
        "save_note": "multi_retriever",
        "disable_save": False,
        "gpu_id": None,
        "use_multi_retriever": True,
        "multi_retriever_setting": {
            "merge_method": args.merge_method,
            "topk": args.topk,
            "retriever_list": [parse_spec(x) for x in args.retriever],
        },
        "framework": "openai",
        "generator_model": "gpt-3.5-turbo",
        "retrieval_topk": args.topk,
        "metrics": ["em", "f1", "acc", "retrieval_recall"],
        "metric_setting": {"retrieval_recall_topk": args.topk},
        "save_intermediate_data": True,
        "save_metric_score": True,
        "refiner_name": None,
    }
    write_yaml(args.output, cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
