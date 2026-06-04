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
    parser.add_argument("--kind", choices=["skr", "adaptive"], required=True)
    parser.add_argument("--training-data", default=None)
    parser.add_argument("--model-path", default=None)
    parser.add_argument("--data-dir", default="dataset")
    parser.add_argument("--dataset-name", default="demo")
    parser.add_argument("--save-dir", required=True)
    args = parser.parse_args()
    if args.kind == "skr":
        judger_config = {
            "model_path": args.model_path or "model/sup-simcse-bert-base-uncased",
            "training_data_path": args.training_data,
            "topk": 5,
            "batch_size": 64,
            "max_length": 128,
        }
    else:
        judger_config = {"model_path": args.model_path or "illuminoplanet/adaptive-rag-classifier", "batch_size": 16, "max_length": 512}
    cfg = {
        "data_dir": args.data_dir,
        "dataset_name": args.dataset_name,
        "split": ["test"],
        "save_dir": args.save_dir,
        "save_note": args.kind,
        "judger_name": "adaptive-rag" if args.kind == "adaptive" else "skr",
        "judger_config": judger_config,
        "retrieval_method": "bm25",
        "bm25_backend": "bm25s",
        "retrieval_topk": 2,
        "metrics": ["em", "f1", "acc"],
    }
    write_yaml(args.output, cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
