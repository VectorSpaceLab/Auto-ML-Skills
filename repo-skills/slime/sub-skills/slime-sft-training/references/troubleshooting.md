# SFT Troubleshooting

## Model Learns Prompt Tokens

Check `step_loss_mask` and data rendering. User/tool/system text should usually be masked.

## `string indices must be integers`

If `sft_rollout` fails inside `mask_utils.py` with:

```text
TypeError: string indices must be integers, not 'str'
```

`sample.prompt` is a string instead of a list of message dictionaries. Remove `--apply-chat-template` for the stock `slime.rollout.sft_rollout.generate_rollout` path and keep the dataset field as OpenAI-style messages.

## Async Driver Assertion

`run_slime_train_async.py` rejects `--colocate`. Use the synchronous runner or remove colocate.

## No SGLang Needed

For basic SFT, use `--debug-train-only` with `sft_rollout`; do not debug SGLang if the job fails before any rollout engine should be used.
