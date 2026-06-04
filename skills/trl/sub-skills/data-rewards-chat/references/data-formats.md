# Data Formats

TRL distinguishes dataset format and dataset type.

- Format: standard strings or conversational message lists.
- Type: language modeling, prompt-only, prompt-completion, preference, unpaired preference, or stepwise supervision.

## Language Modeling

Use with SFT.

Standard:

```python
{"text": "The sky is blue."}
```

Conversational:

```python
{
    "messages": [
        {"role": "user", "content": "What color is the sky?"},
        {"role": "assistant", "content": "It is blue."},
    ]
}
```

## Prompt-Only

Use with GRPO, RLOO, Online DPO, and environment-based workflows.

Standard:

```python
{"prompt": "The sky is"}
```

Conversational:

```python
{"prompt": [{"role": "user", "content": "What color is the sky?"}]}
```

## Prompt-Completion

Use with SFT.

Standard:

```python
{"prompt": "The sky is", "completion": " blue."}
```

Conversational:

```python
{
    "prompt": [{"role": "user", "content": "What color is the sky?"}],
    "completion": [{"role": "assistant", "content": "It is blue."}],
}
```

For prompt-completion SFT, completion-only loss is the default behavior. Set `completion_only_loss=False` only when full-sequence loss is intended.

## Preference

Use with DPO and RewardTrainer. KTO can also accept paired preference data and convert it to unpaired data.

Standard explicit prompt:

```python
{"prompt": "The sky is", "chosen": " blue.", "rejected": " green."}
```

Standard implicit prompt:

```python
{"chosen": "The sky is blue.", "rejected": "The sky is green."}
```

Conversational explicit prompt:

```python
{
    "prompt": [{"role": "user", "content": "What color is the sky?"}],
    "chosen": [{"role": "assistant", "content": "It is blue."}],
    "rejected": [{"role": "assistant", "content": "It is green."}],
}
```

Conversational implicit prompt:

```python
{
    "chosen": [
        {"role": "user", "content": "What color is the sky?"},
        {"role": "assistant", "content": "It is blue."},
    ],
    "rejected": [
        {"role": "user", "content": "What color is the sky?"},
        {"role": "assistant", "content": "It is green."},
    ],
}
```

## Unpaired Preference

Use with KTO-style workflows.

Standard:

```python
{"prompt": "The sky is", "completion": " blue.", "label": True}
```

Conversational:

```python
{
    "prompt": [{"role": "user", "content": "What color is the sky?"}],
    "completion": [{"role": "assistant", "content": "It is green."}],
    "label": False,
}
```

## Stepwise Supervision

Use with process-supervised reward modeling workflows.

```python
{
    "prompt": "Which number is larger, 9.8 or 9.11?",
    "completions": [
        "The fractional part of 9.8 is 0.8.",
        "The fractional part of 9.11 is 0.11.",
        "0.11 is greater than 0.8.",
        "Hence, 9.11 > 9.8.",
    ],
    "labels": [True, True, False, False],
}
```

## Tool Calling Data

For SFT with tool calling, rows should include:

```python
{"messages": messages, "tools": [tool_schema]}
```

Tool schemas should follow the JSON schema format used by Transformers. Prefer generating schemas with:

```python
from transformers.utils import get_json_schema
```

For mixed arbitrary JSON tool arguments, create datasets with `on_mixed_types="use_json"` or explicit `Json()` features when using `datasets>=4.7.0`.

## Multimodal Data

Multimodal conversational content commonly uses message content blocks instead of plain strings. Use TRL helpers:

```python
from trl import prepare_multimodal_messages, prepare_multimodal_messages_vllm
```

For vision-language examples, install the `vlm` extra and inspect the relevant model processor behavior.

## Trainer Mapping

| Dataset type | Stable trainer(s) |
| --- | --- |
| Language modeling | `SFTTrainer` |
| Prompt-completion | `SFTTrainer` |
| Preference | `DPOTrainer`, `RewardTrainer` |
| Prompt-only | `GRPOTrainer`, `RLOOTrainer` |
| Unpaired preference | experimental KTO |
| Stepwise supervision | experimental PRM |
