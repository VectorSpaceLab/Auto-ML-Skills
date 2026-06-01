# Data, Rewards, And Chat Troubleshooting

## Trainer Says Required Columns Are Missing

Inspect a row:

```python
print(dataset[0])
print(dataset.column_names)
```

Then match it to [data formats](data-formats.md). Do not rely on dataset names; inspect actual columns.

## Conversational Rows Are Treated As Plain Strings

Check that values are lists of message dicts:

```python
{"role": "user", "content": "..."}
```

Avoid legacy keys such as `from` and `value` unless you run `maybe_convert_to_chatml`.

## Tool Calling Dataset Fails In `datasets`

Tool calls and tool schemas contain arbitrary JSON. With `datasets>=4.7.0`, use `Dataset.from_list(data, on_mixed_types="use_json")` or explicit `Json()` features. Older versions may need JSON strings.

## Assistant-Only Loss Is Wrong

Causes:

- The chat template lacks generation markers.
- The model family is not recognized by TRL's training-template patcher.
- Dataset rows are not conversational.

Test one row:

```python
rendered = tokenizer.apply_chat_template(messages, tokenize=False)
print(rendered)
```

Then inspect whether assistant spans can be identified.

## Reward Function Shape Error

Reward functions must return one scalar per completion. If there are `N` completions, return a list of length `N`.

```python
def reward_func(completions, **kwargs):
    rewards = [...]
    assert len(rewards) == len(completions)
    return rewards
```

When a reward function also needs labels or solutions, ensure the dataset column name matches the function parameter expected by the built-in reward.

## Rewards Are All `None` Or Zero

Check:

- `math_verify` is installed when using `accuracy_reward` or `reasoning_accuracy_reward`.
- Completion format matches reward parser expectations.
- Solution/label columns are present and not empty.
- For math rewards, answers are in the expected answer tag or parseable form.
- `reward_weights` are not zero.

Use [../scripts/reward_smoke_test.py](../scripts/reward_smoke_test.py) before launching a full training job.

## Multimodal Messages Fail

Check:

- Install `trl[vlm]` for image/video examples.
- Use the model's expected processor class.
- Use `prepare_multimodal_messages` for Transformers workflows and `prepare_multimodal_messages_vllm` for vLLM workflows.
- Do not import multimodal preparation from `trl.chat_template_utils` unless the installed package explicitly exposes it there.

## Packed Data Looks Wrong

Packing is mainly for SFT tokenized/text data. If examples are long and you use `packing_strategy="bfd"`, overflow tokens are discarded. Use `bfd_split` when preserving all tokens matters.
