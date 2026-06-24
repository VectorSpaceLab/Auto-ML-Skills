#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from lf_skill_common import write_yaml


def none_if_empty(value: str | None) -> str | None:
    return None if value in [None, "", "null", "None"] else value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--dataset", default="identity,alpaca_en_demo")
    parser.add_argument("--dataset-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--template", default="qwen3_nothink")
    parser.add_argument("--stage", choices=["sft", "pt"], default="sft")
    parser.add_argument("--freeze-trainable-layers", type=int, default=2)
    parser.add_argument("--freeze-trainable-modules", default="all")
    parser.add_argument("--freeze-extra-modules", default=None)
    parser.add_argument("--use-llama-pro", action="store_true")
    parser.add_argument("--cutoff-len", type=int, default=512)
    parser.add_argument("--max-samples", type=int, default=16)
    parser.add_argument("--max-steps", type=int, default=1)
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    args = parser.parse_args()
    cfg = {
        "model_name_or_path": args.model,
        "trust_remote_code": True,
        "flash_attn": "sdpa",
        "stage": args.stage,
        "do_train": True,
        "finetuning_type": "freeze",
        "freeze_trainable_layers": args.freeze_trainable_layers,
        "freeze_trainable_modules": args.freeze_trainable_modules,
        "freeze_extra_modules": none_if_empty(args.freeze_extra_modules),
        "use_llama_pro": args.use_llama_pro,
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
    }
    write_yaml(args.output, cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
