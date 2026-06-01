#!/usr/bin/env python
"""Print a minimal GRPO environment_factory template.

The printed code is a starting point for environment-based GRPO. It is not
executed by this script.

Example:
    python scripts/openenv_environment_template.py > train_env.py
"""

from __future__ import annotations


TEMPLATE = '''\
from datasets import Dataset
from trl import GRPOConfig, GRPOTrainer


class MyEnv:
    def __init__(self):
        self.reward = 0.0

    def reset(self, **kwargs) -> str | None:
        self.reward = 0.0
        return "Initial observation."

    def submit(self, answer: str) -> str:
        """Submit an answer.

        Args:
            answer: Candidate answer.
        """
        self.reward = 1.0 if answer.strip() == "4" else 0.0
        return "submitted"


def reward_func(environments, **kwargs):
    return [env.reward for env in environments]


dataset = Dataset.from_dict(
    {"prompt": [[{"role": "user", "content": "Use the submit tool to answer: 2 + 2 = ?"}]] * 16}
)

trainer = GRPOTrainer(
    model="Qwen/Qwen3-0.6B",
    args=GRPOConfig(
        output_dir="env-grpo-output",
        num_generations=2,
        max_steps=1,
        log_completions=True,
    ),
    train_dataset=dataset,
    environment_factory=MyEnv,
    reward_funcs=reward_func,
)
trainer.train()
'''


def main() -> int:
    print(TEMPLATE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
