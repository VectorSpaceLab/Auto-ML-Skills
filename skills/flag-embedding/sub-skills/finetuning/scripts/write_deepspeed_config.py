#!/usr/bin/env python3
"""Write DeepSpeed configs used by FlagEmbedding examples.

The generated files are self-contained replacements for the repository example
configs. They use "auto" values expected by Hugging Face Trainer integration.

Examples:
    python scripts/write_deepspeed_config.py --stage 0 --output ds_stage0.json
    python scripts/write_deepspeed_config.py --stage 1 --output ds_stage1.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_config(stage: int) -> dict:
    if stage not in {0, 1}:
        raise ValueError("Only DeepSpeed stages 0 and 1 are bundled.")

    zero_optimization = {"stage": stage}
    if stage == 1:
        zero_optimization["reduce_bucket_size"] = 5e8

    config = {
        "zero_optimization": zero_optimization,
        "fp16": {
            "enabled": "auto",
            "loss_scale": 0,
            "loss_scale_window": 1000,
            "initial_scale_power": 12 if stage == 0 else 10,
            "hysteresis": 2,
            "min_loss_scale": 1,
        },
        "bf16": {"enabled": "auto"},
        "optimizer": {
            "type": "AdamW",
            "params": {
                "lr": "auto",
                "betas": "auto",
                "eps": "auto",
                "weight_decay": "auto",
            },
        },
        "scheduler": {
            "type": "WarmupDecayLR",
            "params": {
                "warmup_min_lr": "auto",
                "warmup_max_lr": "auto",
                "warmup_num_steps": "auto",
                "total_num_steps": "auto",
            },
        },
        "gradient_accumulation_steps": "auto",
        "gradient_clipping": "auto",
        "steps_per_print": 100 if stage == 0 else 1000,
        "train_batch_size": "auto",
        "train_micro_batch_size_per_gpu": "auto",
        "wall_clock_breakdown": False,
    }
    if stage == 1:
        config["bf16"].update(
            {
                "loss_scale": 0,
                "initial_scale_power": 10,
                "loss_scale_window": 1000,
                "hysteresis": 2,
                "min_loss_scale": 1,
            }
        )
        config["optimizer"]["params"]["torch_adam"] = True
    return config


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", type=int, choices=[0, 1], required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    path = Path(args.output)
    path.write_text(json.dumps(build_config(args.stage), indent=2) + "\n", encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
