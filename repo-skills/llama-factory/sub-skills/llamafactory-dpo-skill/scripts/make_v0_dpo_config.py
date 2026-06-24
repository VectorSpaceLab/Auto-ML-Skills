#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import emit


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a default/v0 LLaMA-Factory DPO config.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--dataset", default="dpo_en_demo")
    parser.add_argument("--dataset-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--template", default="qwen3_nothink")
    parser.add_argument("--method", choices=["lora", "full"], default="lora")
    parser.add_argument("--pref-loss", choices=["sigmoid", "orpo", "simpo", "ipo", "hinge"], default="sigmoid")
    parser.add_argument("--pref-beta", type=float, default=0.1)
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--cutoff-len", type=int, default=2048)
    parser.add_argument("--max-samples", type=int, default=1000)
    parser.add_argument("--max-steps", type=int, default=None)
    parser.add_argument("--learning-rate", type=float, default=5e-6)
    parser.add_argument("--per-device-train-batch-size", type=int, default=1)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=8)
    parser.add_argument("--lora-rank", type=int, default=8)
    parser.add_argument("--lora-target", default="all")
    args = parser.parse_args()
    cfg = {
        "model_name_or_path": args.model,
        "trust_remote_code": args.trust_remote_code,
        "flash_attn": "sdpa",
        "stage": "dpo",
        "do_train": True,
        "finetuning_type": args.method,
        "pref_beta": args.pref_beta,
        "pref_loss": args.pref_loss,
        "dataset": args.dataset,
        "dataset_dir": args.dataset_dir,
        "template": args.template,
        "cutoff_len": args.cutoff_len,
        "max_samples": args.max_samples,
        "preprocessing_num_workers": 1,
        "dataloader_num_workers": 0,
        "output_dir": args.output_dir,
        "logging_steps": 1,
        "save_steps": 500,
        "plot_loss": False,
        "overwrite_output_dir": True,
        "save_only_model": False,
        "report_to": "none",
        "per_device_train_batch_size": args.per_device_train_batch_size,
        "gradient_accumulation_steps": args.gradient_accumulation_steps,
        "learning_rate": args.learning_rate,
        "num_train_epochs": 3.0,
        "lr_scheduler_type": "cosine",
        "warmup_ratio": 0.1,
        "bf16": True,
        "ddp_timeout": 180000000,
        "disable_gradient_checkpointing": False,
        "resume_from_checkpoint": None,
    }
    if args.method == "lora":
        cfg["lora_rank"] = args.lora_rank
        cfg["lora_target"] = args.lora_target
    if args.max_steps is not None:
        cfg["max_steps"] = args.max_steps
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(emit(cfg)) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
