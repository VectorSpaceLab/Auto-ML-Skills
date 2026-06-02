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
    parser.add_argument("--save-dir", required=True)
    parser.add_argument("--max-chain-length", type=int, default=3)
    parser.add_argument("--num-chains", type=int, default=4)
    parser.add_argument("--n-context", type=int, default=2)
    parser.add_argument("--triple-load-path", default=None)
    args = parser.parse_args()
    cfg = {
        "data_dir": args.data_dir,
        "dataset_name": args.dataset_name,
        "split": ["test"],
        "save_dir": args.save_dir,
        "save_note": "kg-trace",
        "framework": "hf",
        "refiner_name": "kg-trace",
        "retrieval_method": "bm25",
        "bm25_backend": "bm25s",
        "retrieval_topk": 2,
        "generator_model": "hf-local",
        "generator_model_path": None,
        "metrics": ["em", "f1", "acc"],
        "trace_config": {
            "num_examplars": 3,
            "max_chain_length": args.max_chain_length,
            "topk_triple_select": 5,
            "num_choices": 8,
            "min_triple_prob": 1e-4,
            "num_beams": 3,
            "num_chains": args.num_chains,
            "n_context": args.n_context,
            "context_type": "triples",
            "triple_save_path": str(Path(args.save_dir) / "save_triples.json"),
            "triple_load_path": args.triple_load_path,
        },
        "save_intermediate_data": True,
    }
    write_yaml(args.output, cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
