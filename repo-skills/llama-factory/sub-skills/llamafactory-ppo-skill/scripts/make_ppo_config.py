#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from lf_skill_common import write_yaml


def maybe_path(value: str | None) -> str | None:
    if value in [None, "", "null", "None"]:
        return None
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--dataset", default="identity,alpaca_en_demo")
    parser.add_argument("--dataset-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--template", default="qwen3_nothink")
    parser.add_argument("--method", choices=["lora", "full"], default="lora")
    parser.add_argument("--reward-model", required=True)
    parser.add_argument("--reward-model-type", choices=["lora", "full", "api"], default="full")
    parser.add_argument("--reward-model-adapters", default=None)
    parser.add_argument("--ref-model", default=None)
    parser.add_argument("--cutoff-len", type=int, default=512)
    parser.add_argument("--max-samples", type=int, default=16)
    parser.add_argument("--max-steps", type=int, default=1)
    parser.add_argument("--max-new-tokens", type=int, default=32)
    parser.add_argument("--learning-rate", type=float, default=1e-6)
    parser.add_argument("--ppo-buffer-size", type=int, default=1)
    parser.add_argument("--ppo-epochs", type=int, default=1)
    args = parser.parse_args()
    cfg = {
        "model_name_or_path": args.model,
        "trust_remote_code": True,
        "flash_attn": "sdpa",
        "stage": "ppo",
        "do_train": True,
        "finetuning_type": args.method,
        "reward_model": args.reward_model,
        "reward_model_type": args.reward_model_type,
        "reward_model_adapters": maybe_path(args.reward_model_adapters),
        "ref_model": maybe_path(args.ref_model),
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
        "gradient_accumulation_steps": 1,
        "learning_rate": args.learning_rate,
        "num_train_epochs": 1.0,
        "max_steps": args.max_steps,
        "lr_scheduler_type": "cosine",
        "warmup_ratio": 0.0,
        "bf16": True,
        "ddp_timeout": 180000000,
        "max_new_tokens": args.max_new_tokens,
        "top_k": 0,
        "top_p": 0.9,
        "temperature": 0.7,
        "ppo_buffer_size": args.ppo_buffer_size,
        "ppo_epochs": args.ppo_epochs,
        "ppo_score_norm": False,
        "ppo_target": 6.0,
        "ppo_whiten_rewards": False,
    }
    if args.method == "lora":
        cfg["lora_rank"] = 8
        cfg["lora_target"] = "all"
    write_yaml(args.output, cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
