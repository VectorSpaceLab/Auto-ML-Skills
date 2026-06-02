#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--batch-size", type=int, required=True)
    parser.add_argument("--dataset", default="alpaca_en_demo")
    parser.add_argument("--dataset-dir", required=True)
    parser.add_argument("--template", default="qwen3_nothink")
    parser.add_argument("--stage", choices=["pt", "sft"], default="sft")
    parser.add_argument("--cutoff-len", type=int, default=2048)
    args = parser.parse_args()
    payload = {
        "status": "preflight",
        "model_name_or_path": args.model,
        "batch_size": args.batch_size,
        "dataset": args.dataset,
        "dataset_dir": args.dataset_dir,
        "template": args.template,
        "stage": args.stage,
        "cutoff_len": args.cutoff_len,
        "note": "Learning-rate utility is standalone in the public repo; use this payload to create an equivalent experiment config or vendor the utility.",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
