#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from lf_common import emit_yaml


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a LLaMA-Factory v1 SFT config.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--template", default="qwen3_nothink")
    parser.add_argument("--method", choices=["lora", "full"], default="lora")
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--flash-attn", default="sdpa", choices=["eager", "sdpa", "flash_attention_2"])
    parser.add_argument("--micro-batch-size", type=int, default=1)
    parser.add_argument("--cutoff-len", type=int, default=2048)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--num-train-epochs", type=int, default=3)
    parser.add_argument("--max-steps", type=int, default=None)
    parser.add_argument("--logging-steps", type=int, default=10)
    parser.add_argument("--batching-workers", type=int, default=0)
    parser.add_argument("--bf16", action="store_true", default=True)
    parser.add_argument("--no-bf16", dest="bf16", action="store_false")
    parser.add_argument("--lora-r", type=int, default=8)
    parser.add_argument("--lora-alpha", type=int, default=16)
    parser.add_argument("--lora-dropout", type=float, default=0.05)
    parser.add_argument("--target-modules", default="all")
    args = parser.parse_args()
    cfg = {
        "model": args.model,
        "model_class": "llm",
        "template": args.template,
        "trust_remote_code": args.trust_remote_code,
        "flash_attn": args.flash_attn,
    }
    if args.method == "lora":
        cfg["peft_config"] = {
            "name": "lora",
            "r": args.lora_r,
            "lora_alpha": args.lora_alpha,
            "lora_dropout": args.lora_dropout,
            "target_modules": args.target_modules,
        }
    cfg.update(
        {
            "train_dataset": args.dataset,
            "output_dir": args.output_dir,
            "micro_batch_size": args.micro_batch_size,
            "cutoff_len": args.cutoff_len,
            "learning_rate": args.learning_rate,
            "num_train_epochs": args.num_train_epochs,
            "logging_steps": args.logging_steps,
            "batching_workers": args.batching_workers,
            "bf16": args.bf16,
            "enable_activation_checkpointing": False,
            "save_steps": None,
        }
    )
    if args.max_steps is not None:
        cfg["max_steps"] = args.max_steps
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(emit_yaml(cfg)) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
