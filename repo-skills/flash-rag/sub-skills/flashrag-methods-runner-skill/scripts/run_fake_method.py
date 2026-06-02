#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import read_simple_yaml


def family(method: str) -> str:
    if method in {"naive", "zero-shot"}:
        return "basic-generation"
    if method in {"skr", "adaptive"}:
        return "conditional-judger"
    if method == "trace":
        return "kg-trace"
    if method in {"llmlingua", "recomp", "selective-context"}:
        return "refiner"
    if method.startswith("AAR") or method == "ret-robust":
        return "retrieval-adaptation"
    if method in {"search-r1", "autorefine", "o2-searcher", "r1-searcher", "rearag", "corag", "simpledeepsearcher", "rqrag"}:
        return "reasoning-search"
    return "pipeline"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    cfg = read_simple_yaml(args.config)
    method = str(cfg["method_name"])
    result = {
        "method": method,
        "family": family(method),
        "dataset_name": cfg.get("dataset_name"),
        "sample_num": cfg.get("test_sample_num"),
        "trace": [
            {"step": "load_dataset", "status": "fake-ok"},
            {"step": "configure_method", "status": "fake-ok", "method": method},
            {"step": "run_pipeline", "status": "fake-ok", "prediction": f"fake prediction from {method}"},
        ],
        "metrics": {"acc": 1.0},
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
