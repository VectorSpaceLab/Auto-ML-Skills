#!/usr/bin/env python
"""Smoke-test TRL built-in reward functions on dummy completions.

Example:
    python scripts/reward_smoke_test.py
"""

from __future__ import annotations


def main() -> int:
    from trl.rewards import accuracy_reward, get_soft_overlong_punishment, reasoning_accuracy_reward, think_format_reward

    completions = [
        [{"role": "assistant", "content": r"<think>2 + 2 = 4</think>The answer is \boxed{4}"}],
        [{"role": "assistant", "content": r"<think>I will guess</think>The answer is \boxed{5}"}],
    ]
    solution = ["4", "4"]

    try:
        print("accuracy_reward:", accuracy_reward(completions=completions, solution=solution))
    except ImportError as exc:
        print(f"accuracy_reward skipped: {exc}")
    try:
        print("reasoning_accuracy_reward:", reasoning_accuracy_reward(completions=completions, solution=solution))
    except ImportError as exc:
        print(f"reasoning_accuracy_reward skipped: {exc}")
    print("think_format_reward:", think_format_reward(completions=completions))

    soft_overlong = get_soft_overlong_punishment(max_completion_len=20, soft_punish_cache=5)
    print("soft_overlong:", soft_overlong(completion_ids=[[1, 2, 3], list(range(30))]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
