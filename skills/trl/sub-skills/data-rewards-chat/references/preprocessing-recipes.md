# Preprocessing Recipes

Read this when converting a real dataset into a TRL-compatible schema.

## Convert Instruction Rows To Conversational SFT

Input:

```python
{"instruction": "...", "answer": "..."}
```

Mapping:

```python
def to_messages(example):
    return {
        "messages": [
            {"role": "user", "content": example["instruction"]},
            {"role": "assistant", "content": example["answer"]},
        ]
    }

dataset = dataset.map(to_messages, remove_columns=dataset.column_names)
```

## Convert QA Rows To Prompt-Completion

```python
def to_prompt_completion(example):
    return {
        "prompt": example["question"],
        "completion": example["answer"],
    }
```

Use with `SFTTrainer`.

## Convert Preference Dataset With Custom Columns

Input:

```python
{"input": "...", "accepted": "...", "rejected": "..."}
```

Mapping:

```python
def to_preference(example):
    return {
        "prompt": [{"role": "user", "content": example["input"]}],
        "chosen": [{"role": "assistant", "content": example["accepted"]}],
        "rejected": [{"role": "assistant", "content": example["rejected"]}],
    }
```

Use with DPO or RewardTrainer.

## Extract Prompt From Implicit Preference Data

For preference examples where both `chosen` and `rejected` include the prompt, use:

```python
from trl import maybe_extract_prompt

dataset = dataset.map(maybe_extract_prompt)
```

This can convert implicit preference examples into explicit prompt plus completion columns when possible.

## Convert Preference To Unpaired Preference

```python
from trl import unpair_preference_dataset

unpaired = unpair_preference_dataset(dataset)
```

Use for KTO-style unpaired preference training. `maybe_unpair_preference_dataset` only converts when needed.

## Convert To ChatML-Like Keys

Some datasets use `from` / `value` style records. Use:

```python
from trl import maybe_convert_to_chatml

dataset = dataset.map(maybe_convert_to_chatml)
```

This normalizes messages toward `role` / `content` keys when possible.

## Apply Chat Template

```python
from transformers import AutoTokenizer
from trl import maybe_apply_chat_template

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
dataset = dataset.map(lambda row: maybe_apply_chat_template(row, tokenizer))
```

Most trainers apply templates automatically for conversational datasets. Apply templates manually only when you need explicit control or are preparing offline text fields.

## Pack SFT Data

```python
from trl import pack_dataset

packed = pack_dataset(dataset, seq_length=1024, strategy="bfd")
```

Strategies:

- `bfd`: best-fit decreasing; overlong examples are discarded beyond `seq_length`.
- `bfd_split`: splits long examples before best-fit packing.
- `wrapped`: concatenates all tokens and cuts fixed-length blocks.

For SFT trainer-driven packing, prefer `SFTConfig(packing=True, packing_strategy="bfd")`.

## Tool Calling Dataset

```python
from datasets import Dataset
from transformers.utils import get_json_schema

def search(query: str) -> str:
    """Searches an index.

    Args:
        query: Query string.
    """
    return "result"

tool = get_json_schema(search)
rows = [
    {
        "messages": [
            {"role": "user", "content": "Search for TRL."},
            {"role": "assistant", "tool_calls": [{"type": "function", "function": {"name": "search", "arguments": {"query": "TRL"}}}]},
            {"role": "tool", "name": "search", "content": "TRL is a post-training library."},
            {"role": "assistant", "content": "TRL is a post-training library."},
        ],
        "tools": [tool],
    }
]
dataset = Dataset.from_list(rows, on_mixed_types="use_json")
```

If `datasets` is too old for JSON features, store schemas/arguments as JSON strings or upgrade.
