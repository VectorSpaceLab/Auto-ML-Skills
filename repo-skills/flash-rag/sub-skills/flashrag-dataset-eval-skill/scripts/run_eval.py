#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=None, help="Optional installed package root to add to PYTHONPATH.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--split", default="test")
    parser.add_argument("--prediction-mode", choices=["copy_gold", "from_output", "constant"], default="copy_gold")
    parser.add_argument("--constant-prediction", default="")
    parser.add_argument("--summary", type=Path, default=None)
    args = parser.parse_args()
    if args.package_root is not None:
        sys.path.insert(0, str(args.package_root.resolve()))
    from flashrag.config import Config
    from flashrag.evaluator import Evaluator
    from flashrag.utils import get_dataset

    config = Config(str(args.config))
    split_map = get_dataset(config)
    dataset = split_map[args.split]
    if dataset is None:
        raise FileNotFoundError(f"split not loaded: {args.split}")
    if args.prediction_mode == "copy_gold":
        preds = [answers[0] if answers else "" for answers in dataset.golden_answers]
    elif args.prediction_mode == "from_output":
        preds = []
        for item in dataset:
            preds.append(item.output.get("pred", item.data.get("pred", "")))
    else:
        preds = [args.constant_prediction for _ in dataset]
    dataset.update_output("pred", preds)
    metrics = Evaluator(config).evaluate(dataset)
    payload = {"records": len(dataset), "metrics": metrics, "save_dir": config["save_dir"]}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
