---
name: data-and-rewards
description: "Prepare TRL datasets, chat templates, conversational and multimodal examples, tool-calling schemas, built-in reward functions, custom reward callables, and data utility checks."
---

# Data And Rewards

Use this sub-skill when a user asks about TRL dataset columns, chat templates, tool calling, multimodal messages, packing, preference conversion, or reward functions for GRPO/RLOO.

## Dataset Type Routing

| Task | Required columns |
| --- | --- |
| SFT language modeling | `text` or `messages` |
| SFT prompt-completion | `prompt`, `completion` |
| DPO / RewardTrainer preference | `chosen`, `rejected`, optionally `prompt` |
| KTO unpaired preference | `prompt`, `completion`, `label` |
| GRPO / RLOO prompt-only rewards | `prompt` plus reward-specific columns such as `solution` |
| PRM stepwise supervision | `prompt`, `completions`, `labels` |

Read [references/data-formats.md](references/data-formats.md) for examples and schema conversion notes. Read [references/reward-functions.md](references/reward-functions.md) for built-in reward signatures and custom reward function shape. Run [scripts/inspect_trl_data_utils.py](scripts/inspect_trl_data_utils.py) to inspect available data utilities in the current installed package.

## Standard Vs Conversational

Standard examples use strings:

```python
{"prompt": "The sky is", "completion": " blue."}
```

Conversational examples use role/content messages:

```python
{
    "prompt": [{"role": "user", "content": "What color is the sky?"}],
    "completion": [{"role": "assistant", "content": "It is blue."}],
}
```

TRL trainers automatically apply chat templates for conversational datasets when given an appropriate tokenizer or processor.

## Useful Utilities

```python
from trl import (
    apply_chat_template,
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

Use utility functions for structured conversion rather than ad hoc string manipulation.

## Built-In Rewards

```python
from trl.rewards import (
    accuracy_reward,
    reasoning_accuracy_reward,
    think_format_reward,
    get_soft_overlong_punishment,
)
```

For GRPO/RLOO, reward functions must return reward values aligned with generated completions. Inspect rewards on a tiny batch before training.

## Tool Calling

For SFT with tool calling, conversational rows include `messages` and a `tools` column containing JSON-schema tool descriptions. Use `transformers.utils.get_json_schema` to generate schemas from Python functions.

When using `datasets.Dataset.from_list` with mixed JSON tool arguments, use `on_mixed_types="use_json"` or explicit `datasets.Features` with `Json` if available.

## Chat Templates

For `assistant_only_loss=True`, the chat template must include generation markers that let the tokenizer return assistant-token masks. TRL provides training templates for common model families. If masks are wrong, use `chat_template_path` or the chat-template utilities instead of trying to patch rendered strings after tokenization.

For vLLM multimodal paths, use `prepare_multimodal_messages_vllm` and verify the expected image/video structure before serving or training.
