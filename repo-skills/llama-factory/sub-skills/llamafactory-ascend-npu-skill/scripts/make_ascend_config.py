#!/usr/bin/env python3
"""Emit a minimal LLaMA-Factory Ascend NPU training YAML.

Usage:
  python scripts/make_ascend_config.py --recipe qwen-full --model Qwen/Qwen3-8B --dataset alpaca_en_demo

The script prints a public, editable YAML snippet. It does not import
LLaMA-Factory and does not start training.
"""

from __future__ import annotations

import argparse


RECIPES = {
    "qwen-full": {"template": "qwen3", "finetuning_type": "full", "flash_attn": "fa2"},
    "qwen-moe-full": {"template": "qwen3", "finetuning_type": "full", "flash_attn": "fa2", "save_only_model": "true"},
    "qwen-vl-full": {"template": "qwen3_vl", "finetuning_type": "full", "flash_attn": "fa2", "vl": True},
    "qwen-vl-lora": {"template": "qwen3_vl", "finetuning_type": "lora", "flash_attn": "disabled", "vl": True},
    "qwen-qlora": {"template": "qwen3", "finetuning_type": "lora", "flash_attn": "fa2", "quantization_bit": 4},
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an Ascend NPU LLaMA-Factory YAML snippet.")
    parser.add_argument("--recipe", choices=sorted(RECIPES), default="qwen-full")
    parser.add_argument("--model", default="Qwen/Qwen3-8B")
    parser.add_argument("--dataset", default="alpaca_en_demo")
    parser.add_argument("--output-dir", default="saves/qwen/npu")
    parser.add_argument("--max-steps", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=1)
    args = parser.parse_args()

    recipe = RECIPES[args.recipe]
    lines = [
        "### model",
        f"model_name_or_path: {args.model}",
        "trust_remote_code: true",
        "use_v1_kernels: true",
        f"flash_attn: {recipe['flash_attn']}",
    ]
    if recipe.get("vl"):
        lines += ["image_max_pixels: 262144", "video_max_pixels: 16384"]
    if "quantization_bit" in recipe:
        lines += [f"quantization_bit: {recipe['quantization_bit']}"]

    lines += [
        "",
        "### method",
        "stage: sft",
        "do_train: true",
        f"finetuning_type: {recipe['finetuning_type']}",
    ]
    if recipe["finetuning_type"] == "lora":
        lines += ["lora_rank: 8", "lora_target: all"]

    lines += [
        "",
        "### dataset",
        f"dataset: {args.dataset}",
        f"template: {recipe['template']}",
        "cutoff_len: 2048",
        "overwrite_cache: true",
        "preprocessing_num_workers: 8",
        "dataloader_num_workers: 4",
        "",
        "### output",
        f"output_dir: {args.output_dir}",
        "logging_steps: 1",
        "save_steps: 100",
        f"max_steps: {args.max_steps}",
        "plot_loss: true",
        "overwrite_output_dir: true",
        f"save_only_model: {recipe.get('save_only_model', 'false')}",
        "report_to: none",
        "",
        "### train",
        f"per_device_train_batch_size: {args.batch_size}",
        f"gradient_accumulation_steps: {args.grad_accum}",
        "learning_rate: 1.0e-5",
        "lr_scheduler_type: cosine",
        "warmup_ratio: 0.1",
        "bf16: true",
        "ddp_timeout: 180000000",
        "resume_from_checkpoint: null",
    ]
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
