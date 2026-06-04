#!/usr/bin/env python
"""Generate a minimal TRL CLI YAML config for a training command.

The script writes YAML to stdout. It has no dependency on TRL and no side
effects beyond printing.

Examples:
    python scripts/make_trl_config.py sft --model Qwen/Qwen2.5-0.5B --dataset trl-lib/Capybara
    python scripts/make_trl_config.py grpo --model Qwen/Qwen2.5-0.5B-Instruct --dataset trl-lib/DeepMath-103K
"""

from __future__ import annotations

import argparse


def emit_line(key: str, value: object) -> None:
    if isinstance(value, bool):
        text = "true" if value else "false"
    elif isinstance(value, (int, float)):
        text = str(value)
    else:
        text = str(value)
    print(f"{key}: {text}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["sft", "dpo", "grpo", "rloo", "reward", "kto"])
    parser.add_argument("--model", default="Qwen/Qwen2.5-0.5B", help="Model id or path.")
    parser.add_argument("--dataset", default=None, help="Dataset id or path.")
    parser.add_argument("--output-dir", default=None, help="Output directory.")
    args = parser.parse_args()

    dataset_defaults = {
        "sft": "trl-lib/Capybara",
        "dpo": "trl-lib/ultrafeedback_binarized",
        "grpo": "trl-lib/DeepMath-103K",
        "rloo": "trl-lib/DeepMath-103K",
        "reward": "trl-lib/ultrafeedback_binarized",
        "kto": "trl-lib/kto-mix-14k",
    }
    learning_rates = {
        "sft": "2.0e-5",
        "dpo": "1.0e-6",
        "grpo": "1.0e-6",
        "rloo": "1.0e-6",
        "reward": "1.0e-4",
        "kto": "1.0e-6",
    }

    emit_line("model_name_or_path", args.model)
    emit_line("dataset_name", args.dataset or dataset_defaults[args.command])
    emit_line("output_dir", args.output_dir or f"{args.command}-output")
    emit_line("learning_rate", learning_rates[args.command])
    emit_line("per_device_train_batch_size", 2)
    emit_line("gradient_accumulation_steps", 8)

    if args.command == "sft":
        emit_line("max_length", 1024)
    elif args.command == "dpo":
        emit_line("max_length", 1024)
        emit_line("beta", 0.1)
    elif args.command in {"grpo", "rloo"}:
        print("reward_funcs:")
        print("  - accuracy_reward")
        emit_line("num_generations", 8 if args.command == "grpo" else 2)
        emit_line("max_completion_length", 256)
    elif args.command == "reward":
        emit_line("max_length", 1024)
    elif args.command == "kto":
        emit_line("beta", 0.1)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
