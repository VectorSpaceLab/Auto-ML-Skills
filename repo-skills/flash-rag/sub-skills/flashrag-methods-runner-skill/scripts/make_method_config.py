#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import write_yaml


METHODS = {
    "naive",
    "zero-shot",
    "AAR-contriever",
    "AAR-ANCE",
    "llmlingua",
    "recomp",
    "selective-context",
    "ret-robust",
    "sure",
    "replug",
    "skr",
    "selfrag",
    "flare",
    "iterretgen",
    "ircot",
    "trace",
    "adaptive",
    "rqrag",
    "r1-searcher",
    "search-r1",
    "autorefine",
    "o2-searcher",
    "rearag",
    "corag",
    "simpledeepsearcher",
}


def method_overrides(method: str) -> dict:
    if method == "zero-shot":
        return {"use_retrieval_cache": False, "retrieval_topk": 0, "save_note": "zero-shot"}
    if method.startswith("AAR"):
        return {"retrieval_method": method, "index_path": f"{method}_Flat.index", "save_note": method}
    if method == "llmlingua":
        return {"refiner_name": "longllmlingua", "llmlingua_config": {"rate": 0.55}, "save_note": "longllmlingua"}
    if method == "recomp":
        return {"refiner_name": "recomp-abstractive", "refiner_topk": 5, "save_note": "recomp-abstractive"}
    if method == "selective-context":
        return {"refiner_name": "selective-context", "sc_config": {"reduce_ratio": 0.5}, "save_note": "selective-context"}
    if method == "skr":
        return {"judger_name": "skr", "judger_config": {"training_data_path": "sample_data/skr_training.json", "topk": 5}, "save_note": "skr"}
    if method == "adaptive":
        return {"judger_name": "adaptive-rag", "judger_config": {"model_path": "illuminoplanet/adaptive-rag-classifier"}, "save_note": "adaptive-rag"}
    if method == "trace":
        return {"refiner_name": "kg-trace", "framework": "hf", "trace_config": {"max_chain_length": 4, "n_context": 5}, "save_note": "trace"}
    if method in {"search-r1", "autorefine", "o2-searcher", "r1-searcher", "rearag", "corag", "simpledeepsearcher"}:
        return {"framework": "vllm", "is_reasoning": True, "save_note": method}
    return {"save_note": method}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--method", choices=sorted(METHODS), required=True)
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--split", default="test")
    parser.add_argument("--save-dir", required=True)
    parser.add_argument("--sample-num", type=int, default=3)
    args = parser.parse_args()
    cfg = {
        "method_name": args.method,
        "data_dir": args.data_dir,
        "dataset_name": args.dataset_name,
        "split": [args.split],
        "save_dir": args.save_dir,
        "gpu_id": None,
        "framework": "openai",
        "generator_model": "gpt-3.5-turbo",
        "generator_model_path": None,
        "generation_params": {"max_tokens": 64},
        "retrieval_method": "bm25",
        "bm25_backend": "bm25s",
        "retrieval_topk": 2,
        "metrics": ["em", "f1", "acc"],
        "test_sample_num": args.sample_num,
        "save_intermediate_data": True,
    }
    cfg.update(method_overrides(args.method))
    write_yaml(args.output, cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
