#!/usr/bin/env python
"""Smoke-test installed TRL trainer/config imports without downloading models.

The script constructs configs and exercises built-in reward functions on dummy
inputs. It does not instantiate model weights or call train().

Example:
    python sub-skills/training/scripts/trainer_smoke_test.py
"""

from __future__ import annotations

import inspect


def print_signature(name: str, obj: object) -> None:
    try:
        signature = inspect.signature(obj)
    except Exception as exc:
        signature = f"unavailable: {exc.__class__.__name__}: {exc}"
    print(f"{name}: {signature}")


def main() -> int:
    import trl

    expected = [
        "SFTTrainer",
        "SFTConfig",
        "DPOTrainer",
        "DPOConfig",
        "GRPOTrainer",
        "GRPOConfig",
        "RLOOTrainer",
        "RLOOConfig",
        "RewardTrainer",
        "RewardConfig",
    ]
    missing = [name for name in expected if not hasattr(trl, name)]
    if missing:
        print(f"missing expected TRL objects: {missing}")
        return 1

    print(f"trl version: {getattr(trl, '__version__', 'unknown')}")
    for name in expected:
        print_signature(name, getattr(trl, name))

    configs = [
        trl.SFTConfig(output_dir="tmp-sft", max_steps=1),
        trl.DPOConfig(output_dir="tmp-dpo", max_steps=1),
        trl.GRPOConfig(output_dir="tmp-grpo", max_steps=1, num_generations=2),
        trl.RLOOConfig(output_dir="tmp-rloo", max_steps=1, num_generations=2),
        trl.RewardConfig(output_dir="tmp-reward", max_steps=1),
    ]
    print("constructed configs:", ", ".join(type(config).__name__ for config in configs))

    from trl.rewards import accuracy_reward, get_soft_overlong_punishment, think_format_reward

    completions = [
        [{"role": "assistant", "content": "<think>2 + 2 = 4</think><answer>4</answer>"}],
        [{"role": "assistant", "content": "plain answer"}],
    ]
    try:
        print("accuracy_reward:", accuracy_reward(completions=completions, solution=["4", "4"]))
    except ImportError as exc:
        print(f"accuracy_reward skipped: {exc}")
    print("think_format_reward:", think_format_reward(completions=completions))
    soft_overlong = get_soft_overlong_punishment(max_completion_len=20, soft_punish_cache=5)
    print("soft_overlong:", soft_overlong(completion_ids=[[1, 2, 3], list(range(30))]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
