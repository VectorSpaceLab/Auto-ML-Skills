---
name: trl-data-rewards-chat
description: Prepare TRL datasets, chat templates, tool-calling rows, multimodal messages, preprocessing utilities, and reward functions.
license: Apache-2.0
---

# TRL Data, Rewards, And Chat

Use this sub-skill when a task involves TRL dataset formats, chat templates, tool calling, multimodal data, reward functions, preprocessing helpers, or data-shape troubleshooting.

## Core Rule

Pick the dataset type before picking the trainer:

- Language modeling: `text` or `messages`.
- Prompt-only: `prompt`.
- Prompt-completion: `prompt` and `completion`.
- Preference: `chosen` and `rejected`, optionally `prompt`.
- Unpaired preference: `prompt`, `completion`, and `label`.
- Stepwise supervision: `prompt`, `completions`, and `labels`.

Read [references/data-formats.md](references/data-formats.md) for examples and trainer mapping.

## Trainer Mapping

| Data type | Use with |
| --- | --- |
| Language modeling | SFT |
| Prompt-completion | SFT |
| Preference | DPO or RewardTrainer |
| Prompt-only | GRPO, RLOO, or experimental online methods |
| Unpaired preference | experimental KTO |
| Stepwise supervision | experimental PRM |

## Utility Imports

```python
from trl import (
    apply_chat_template,
    extract_prompt,
    is_conversational,
    maybe_apply_chat_template,
    maybe_convert_to_chatml,
    maybe_extract_prompt,
    maybe_unpair_preference_dataset,
    pack_dataset,
    prepare_multimodal_messages,
    prepare_multimodal_messages_vllm,
    unpair_preference_dataset,
)
```

Chat-template helpers:

```python
from trl import clone_chat_template, get_training_chat_template, supports_tool_calling
```

Reward functions:

```python
from trl.rewards import accuracy_reward, reasoning_accuracy_reward, think_format_reward, get_soft_overlong_punishment
```

## Short Workflow

1. Inspect a sample row and identify the dataset type.
2. Validate columns and value shapes with [scripts/validate_dataset_jsonl.py](scripts/validate_dataset_jsonl.py) for local JSONL or equivalent checks for a Hub dataset sample.
3. Convert conversational rows to the expected schema before training.
4. For SFT assistant-only loss and GRPO tool calling, verify the chat template behavior.
5. Smoke-test custom rewards with a tiny list of completions before launching training. Use [scripts/reward_smoke_test.py](scripts/reward_smoke_test.py) for built-ins.

## Tool Calling

Tool-calling SFT data should include `messages` plus a `tools` column containing JSON schemas. Generate schemas from Python functions with `transformers.utils.get_json_schema` where possible. With `datasets>=4.7.0`, prefer `Json()` features for tool arguments and schemas.

For GRPO tools or environments, switch to [experimental-agents](../experimental-agents/SKILL.md).

## References

- [references/data-formats.md](references/data-formats.md): Standard and conversational schemas for each dataset type.
- [references/rewards-and-chat-templates.md](references/rewards-and-chat-templates.md): Built-in rewards, custom reward contracts, chat-template requirements, tool calling, and multimodal notes.
- [references/preprocessing-recipes.md](references/preprocessing-recipes.md): Common conversion, packing, unpairing, and ChatML recipes.
- [references/troubleshooting.md](references/troubleshooting.md): Data, template, reward, and multimodal failure modes.
