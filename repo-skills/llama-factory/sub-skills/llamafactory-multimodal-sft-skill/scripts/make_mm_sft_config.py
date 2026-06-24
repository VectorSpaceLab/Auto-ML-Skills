#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from lf_skill_common import write_yaml


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a LLaMA-Factory multimodal SFT config.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--dataset", default="mllm_demo,identity")
    parser.add_argument("--dataset-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--template", default="qwen3_vl_nothink")
    parser.add_argument("--method", choices=["lora", "full"], default="lora")
    parser.add_argument("--image-max-pixels", type=int, default=262144)
    parser.add_argument("--video-max-pixels", type=int, default=16384)
    parser.add_argument("--freeze-vision-tower", action="store_true")
    parser.add_argument("--freeze-projector", action="store_true")
    parser.add_argument("--cutoff-len", type=int, default=2048)
    parser.add_argument("--max-samples", type=int, default=1000)
    parser.add_argument("--max-steps", type=int, default=None)
    args = parser.parse_args()
    cfg = {
        "model_name_or_path": args.model,
        "image_max_pixels": args.image_max_pixels,
        "video_max_pixels": args.video_max_pixels,
        "trust_remote_code": True,
        "flash_attn": "sdpa",
        "stage": "sft",
        "do_train": True,
        "finetuning_type": args.method,
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
        "gradient_accumulation_steps": 2,
        "learning_rate": 1e-4 if args.method == "lora" else 1e-5,
        "num_train_epochs": 3.0,
        "lr_scheduler_type": "cosine",
        "warmup_ratio": 0.1,
        "bf16": True,
        "ddp_timeout": 180000000,
    }
    if args.method == "lora":
        cfg["lora_rank"] = 8
        cfg["lora_target"] = "all"
    if args.freeze_vision_tower:
        cfg["freeze_vision_tower"] = True
    if args.freeze_projector:
        cfg["freeze_multi_modal_projector"] = True
    if args.max_steps is not None:
        cfg["max_steps"] = args.max_steps
    write_yaml(args.output, cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
