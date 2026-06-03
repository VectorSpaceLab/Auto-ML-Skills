#!/usr/bin/env python3
"""Emit a minimal LLaMA-Factory KTransformers MoE LoRA training YAML."""

from __future__ import annotations

import argparse


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a KTransformers training YAML snippet.")
    parser.add_argument("--model", default="Qwen/Qwen3-235B-A22B-Instruct-2507")
    parser.add_argument("--template", default="qwen3")
    parser.add_argument("--dataset", default="identity,alpaca_en_demo")
    parser.add_argument("--output-dir", default="saves/kt_moe_lora")
    parser.add_argument("--lora-rank", type=int, default=8)
    parser.add_argument("--kt-weight-path", default="")
    args = parser.parse_args()

    lines = [
        "### model",
        f"model_name_or_path: {args.model}",
        "trust_remote_code: true",
        "",
        "### method",
        "stage: sft",
        "do_train: true",
        "finetuning_type: lora",
        f"lora_rank: {args.lora_rank}",
        "lora_target: all",
        "",
        "### dataset",
        f"dataset: {args.dataset}",
        f"template: {args.template}",
        "cutoff_len: 2048",
        "overwrite_cache: true",
        "preprocessing_num_workers: 8",
        "dataloader_num_workers: 4",
        "",
        "### output",
        f"output_dir: {args.output_dir}",
        "logging_steps: 10",
        "save_steps: 500",
        "plot_loss: true",
        "overwrite_output_dir: true",
        "save_only_model: false",
        "report_to: none",
        "",
        "### train",
        "per_device_train_batch_size: 1",
        "gradient_accumulation_steps: 8",
        "learning_rate: 1.0e-4",
        "num_train_epochs: 1.0",
        "lr_scheduler_type: cosine",
        "warmup_ratio: 0.1",
        "bf16: true",
        "ddp_timeout: 180000000",
        "resume_from_checkpoint: null",
        "",
        "### ktransformers",
        "use_kt: true",
    ]
    if args.kt_weight_path:
        lines.append(f"kt_weight_path: {args.kt_weight_path}")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
