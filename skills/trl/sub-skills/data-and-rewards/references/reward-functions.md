# Reward Functions

Read this when configuring GRPO/RLOO rewards or debugging reward outputs.

## Built-In Rewards

TRL exposes these built-ins from `trl.rewards`:

```python
from trl.rewards import (
    accuracy_reward,
    reasoning_accuracy_reward,
    think_format_reward,
    get_soft_overlong_punishment,
)
```

Verified signatures:

```python
accuracy_reward(
    completions: list[list[dict[str, str]]],
    solution: list[str],
    log_extra=None,
    **kwargs,
) -> list[float | None]
```

```python
reasoning_accuracy_reward(
    completions: list[list[dict[str, str]]],
    solution: list[str],
    reasoning_delimiters: list[str] | None = None,
    log_extra=None,
    **kwargs,
) -> list[float | None]
```

```python
think_format_reward(completions: list[list[dict[str, str]]], **kwargs) -> list[float]
```

```python
get_soft_overlong_punishment(max_completion_len: int, soft_punish_cache: int) -> Callable
```

## Custom Reward Shape

For GRPO/RLOO, a reward function commonly receives generated completions plus any dataset columns whose names match function parameters:

```python
def reward_func(completions, solution, **kwargs):
    rewards = []
    for completion, target in zip(completions, solution):
        text = completion[0]["content"] if isinstance(completion, list) else str(completion)
        rewards.append(1.0 if target in text else 0.0)
    return rewards
```

Use `None` for examples that should be skipped or cannot be scored when the trainer supports nullable reward outputs.

## Reward Models

Instead of Python callables, online trainers can use reward model identifiers or model objects through `reward_funcs` / `reward_model_name_or_path`. If using multiple rewards, align `reward_processing_classes` and `reward_weights` with the reward list.

## Debugging Rewards

Before training:

```python
sample_completions = [[{"role": "assistant", "content": "The answer is 4."}]]
print(accuracy_reward(sample_completions, solution=["4"]))
```

Checks:

- Return length must match the number of scored completions.
- Reward scale should be meaningful. All-zero or all-one rewards produce weak learning signals.
- For reasoning rewards, ensure delimiters and final answer parsing match the generated format.
- For multiple rewards, log each component and the weighted sum.
- If `frac_reward_zero_std` is high in GRPO/RLOO metrics, all completions for many prompts are receiving the same reward.
