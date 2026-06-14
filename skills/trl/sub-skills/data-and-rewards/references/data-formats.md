# Data Formats

Read this when preparing datasets for TRL trainers.

## Standard Formats

Language modeling:

```python
{"text": "The sky is blue."}
```

Prompt-only:

```python
{"prompt": "The sky is"}
```

Prompt-completion:

```python
{"prompt": "The sky is", "completion": " blue."}
```

Preference with explicit prompt:

```python
{"prompt": "The sky is", "chosen": " blue.", "rejected": " green."}
```

Preference with implicit prompt:

```python
{"chosen": "The sky is blue.", "rejected": "The sky is green."}
```

Unpaired preference:

```python
{"prompt": "The sky is", "completion": " blue.", "label": True}
```

Stepwise supervision:

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

## Conversational Formats

Use lists of message dictionaries:

```python
messages = [
    {"role": "user", "content": "Hello."},
    {"role": "assistant", "content": "How can I help?"},
]
```

Conversational prompt-completion:

```python
{
    "prompt": [{"role": "user", "content": "What color is the sky?"}],
    "completion": [{"role": "assistant", "content": "It is blue."}],
}
```

Conversational preference:

```python
{
    "prompt": [{"role": "user", "content": "What color is the sky?"}],
    "chosen": [{"role": "assistant", "content": "It is blue."}],
    "rejected": [{"role": "assistant", "content": "It is green."}],
}
```

Implicit conversational preference:

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

## Trainer Compatibility

| Trainer | Compatible data |
| --- | --- |
| `SFTTrainer` | language modeling, prompt-completion; standard or conversational |
| `DPOTrainer` | preference; standard or conversational, explicit or implicit prompt |
| `RewardTrainer` | preference; standard or conversational, explicit or implicit prompt |
| `GRPOTrainer` | prompt-only plus reward columns; standard or conversational prompts |
| `RLOOTrainer` | prompt-only plus reward columns; standard or conversational prompts |
| `KTOTrainer` | unpaired preference; may convert paired preference to unpaired |

## Tool Calling

Tool-calling datasets use messages with assistant `tool_calls`, tool responses, and a `tools` column:

```python
from transformers.utils import get_json_schema

def control_light(room: str, state: str) -> str:
    """Controls room lights."""
    return f"The lights in {room} are now {state}."

row = {
    "messages": [
        {"role": "user", "content": "Turn on the living room lights."},
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "type": "function",
                    "function": {"name": "control_light", "arguments": {"room": "living room", "state": "on"}},
                }
            ],
        },
        {"role": "tool", "name": "control_light", "content": "The lights in the living room are now on."},
        {"role": "assistant", "content": "Done."},
    ],
    "tools": [get_json_schema(control_light)],
}
```

Use `Dataset.from_list(..., on_mixed_types="use_json")` or explicit `datasets.Json` features when tool arguments contain arbitrary JSON.

## Conversion Utilities

- `maybe_convert_to_chatml(example)`: normalize common chat formats.
- `maybe_extract_prompt(example)`: split implicit prompt from preference data when possible.
- `unpair_preference_dataset(dataset)`: convert paired preference rows into unpaired rows.
- `maybe_unpair_preference_dataset(dataset)`: convert only when needed.
- `pack_dataset(dataset, seq_length, strategy="bfd")`: pack SFT examples for efficiency.

Inspect one row before and after conversion. Most TRL data bugs are column-shape bugs, not model bugs.
