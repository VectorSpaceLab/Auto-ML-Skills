#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from lf_skill_common import write_yaml


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a distributed LLaMA-Factory default-trainer config.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--dataset", default="identity,alpaca_en_demo")
    parser.add_argument("--dataset-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--stage", choices=["sft", "pt", "rm", "dpo", "kto"], default="sft")
    parser.add_argument("--template", default="qwen3_nothink")
    parser.add_argument("--finetuning-type", choices=["full", "lora", "freeze"], default="full")
    parser.add_argument("--deepspeed", default=None)
    parser.add_argument("--ray-num-workers", type=int, default=None)
    parser.add_argument("--cutoff-len", type=int, default=2048)
    parser.add_argument("--max-samples", type=int, default=1000)
    parser.add_argument("--max-steps", type=int, default=None)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=2)
    parser.add_argument("--learning-rate", type=float, default=1e-5)
    args = parser.parse_args()
    cfg = {
        "model_name_or_path": args.model,
        "trust_remote_code": True,
        "flash_attn": "sdpa",
        "stage": args.stage,
        "do_train": True,
        "finetuning_type": args.finetuning_type,
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
        "per_device_train_batch_size": 1,
        "gradient_accumulation_steps": args.gradient_accumulation_steps,
        "learning_rate": args.learning_rate,
        "num_train_epochs": 3.0,
        "lr_scheduler_type": "cosine",
        "warmup_ratio": 0.1,
        "bf16": True,
        "ddp_timeout": 180000000,
    }
    if args.finetuning_type == "lora":
        cfg["lora_rank"] = 8
        cfg["lora_target"] = "all"
    if args.deepspeed:
        cfg["deepspeed"] = args.deepspeed
    if args.ray_num_workers:
        cfg["ray_num_workers"] = args.ray_num_workers
    if args.max_steps is not None:
        cfg["max_steps"] = args.max_steps
    write_yaml(args.output, cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
