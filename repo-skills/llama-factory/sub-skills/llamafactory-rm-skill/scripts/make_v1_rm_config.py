#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from lf_common import emit


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--template", default="qwen3_nothink")
    parser.add_argument("--method", choices=["full", "lora"], default="full")
    parser.add_argument("--cutoff-len", type=int, default=2048)
    parser.add_argument("--max-steps", type=int, default=None)
    parser.add_argument("--learning-rate", type=float, default=1e-6)
    args = parser.parse_args()
    cfg = {
        "model": args.model,
        "model_class": "cls",
        "template": args.template,
        "trust_remote_code": True,
        "flash_attn": "sdpa",
    }
    if args.method == "lora":
        cfg["peft_config"] = {"name": "lora", "r": 8, "lora_alpha": 16, "lora_dropout": 0.05, "target_modules": "all"}
    cfg.update(
        {
            "train_dataset": args.dataset,
            "output_dir": args.output_dir,
            "micro_batch_size": 1,
            "cutoff_len": args.cutoff_len,
            "learning_rate": args.learning_rate,
            "num_train_epochs": 3,
            "logging_steps": 1,
            "bf16": True,
            "enable_activation_checkpointing": False,
            "batching_workers": 0,
            "save_steps": None,
        }
    )
    if args.max_steps is not None:
        cfg["max_steps"] = args.max_steps
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(emit(cfg)) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
