#!/usr/bin/env python3
"""Emit a minimal LLaMA-Factory Megatron-Core full-training YAML."""

from __future__ import annotations

import argparse


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a Megatron-Core LLaMA-Factory YAML snippet.")
    parser.add_argument("--recipe", choices=["qwen-vl", "qwen-moe"], default="qwen-moe")
    parser.add_argument("--model", default="")
    parser.add_argument("--dataset", default="")
    parser.add_argument("--output-dir", default="saves/mcore/full")
    parser.add_argument("--tp", type=int, default=1)
    parser.add_argument("--pp", type=int, default=4)
    parser.add_argument("--ep", type=int, default=2)
    args = parser.parse_args()

    if args.recipe == "qwen-vl":
        model = args.model or "Qwen/Qwen2-VL-7B-Instruct"
        dataset = args.dataset or "llava_1k_en"
        template = "qwen2_vl"
        extra_model = ["image_max_pixels: 262144", "video_max_pixels: 16384"]
        extra_mcore = ["sequence_parallel: true"]
    else:
        model = args.model or "Qwen/Qwen3-30B-A3B-Instruct-2507"
        dataset = args.dataset or "alpaca_en_demo"
        template = "qwen3_nothink"
        extra_model = []
        extra_mcore = [
            "sequence_parallel: false",
            "overlap_param_gather: true",
            "overlap_grad_reduce: true",
            "moe_grouped_gemm: true",
            "moe_token_dispatcher_type: alltoall",
            f"expert_model_parallel_size: {args.ep}",
            "recompute_granularity: full",
        ]

    lines = [
        f"model_name_or_path: {model}",
        *extra_model,
        "",
        "do_train: true",
        "stage: sft",
        "finetuning_type: full",
        f"dataset: {dataset}",
        "preprocessing_num_workers: 8",
        "cutoff_len: 4096",
        f"template: {template}",
        "",
        f"output_dir: {args.output_dir}",
        "per_device_train_batch_size: 1",
        "gradient_accumulation_steps: 8",
        "num_train_epochs: 1",
        "learning_rate: 3e-6",
        "logging_steps: 1",
        "save_steps: 100",
        "lr_scheduler_type: constant",
        "bf16: true",
        "",
        f"tensor_model_parallel_size: {args.tp}",
        f"pipeline_model_parallel_size: {args.pp}",
        "bias_activation_fusion: true",
        "apply_rope_fusion: true",
        "use_distributed_optimizer: true",
        *extra_mcore,
    ]
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
