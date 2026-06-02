#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--dataset", default="alpaca_en_demo")
    parser.add_argument("--dataset-dir", required=True)
    parser.add_argument("--template", default="qwen3_nothink")
    parser.add_argument("--stage", choices=["pt", "sft", "rm"], default="sft")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-samples", type=int, default=None)
    parser.add_argument("--log", type=Path, default=None)
    args = parser.parse_args()
    payload = {
        "status": "handoff",
        "reason": "Perplexity calculation is a standalone LLaMA-Factory utility, not a stable installed-package CLI.",
        "model_name_or_path": args.model,
        "dataset": args.dataset,
        "dataset_dir": args.dataset_dir,
        "template": args.template,
        "stage": args.stage,
        "max_samples": args.max_samples,
        "next_step": "For package-only workflows, generate a short evaluation/prediction config and compute loss from trainer outputs; for exact utility behavior, vendor the public cal_ppl utility into the working project.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
