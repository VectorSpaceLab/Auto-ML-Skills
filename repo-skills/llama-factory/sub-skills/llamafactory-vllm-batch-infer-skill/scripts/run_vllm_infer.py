#!/usr/bin/env python3
"""Prepare a self-contained vLLM batch inference handoff.

LLaMA-Factory exposes vLLM batch inference as a standalone utility in the public
repository, not as a stable package CLI. This script records the validated
parameters and the equivalent call shape so an agent can either vendor/adapt the
utility or switch to the inference sub-skill's package-backed prediction path.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("vllm_infer_handoff.json"))
    parser.add_argument("--model", required=True)
    parser.add_argument("--adapter", default=None)
    parser.add_argument("--dataset", default="alpaca_en_demo")
    parser.add_argument("--dataset-dir", required=True)
    parser.add_argument("--template", default="qwen3_nothink")
    parser.add_argument("--max-samples", type=int, default=None)
    parser.add_argument("--save-name", type=Path, default=Path("generated_predictions.jsonl"))
    parser.add_argument("--max-new-tokens", type=int, default=128)
    parser.add_argument("--log", type=Path, default=None)
    args = parser.parse_args()

    payload = {
        "status": "handoff",
        "reason": "LLaMA-Factory vLLM batch inference is a standalone utility, not a stable installed-package CLI.",
        "model_name_or_path": args.model,
        "adapter_name_or_path": args.adapter,
        "dataset": args.dataset,
        "dataset_dir": args.dataset_dir,
        "template": args.template,
        "max_samples": args.max_samples,
        "save_name": str(args.save_name),
        "max_new_tokens": args.max_new_tokens,
        "next_steps": [
            "For package-only execution, use the inference sub-skill to generate a do_predict config and run `python -m llamafactory.cli train <predict.yaml>`.",
            "For true vLLM batch inference, vendor an adapted copy of the public vllm_infer utility into the working project and pass these parameters.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
