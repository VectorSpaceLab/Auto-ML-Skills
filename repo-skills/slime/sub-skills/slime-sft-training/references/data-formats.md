# SFT Data Formats

## OpenAI Messages

```json
{"messages":[{"role":"user","content":"Write a haiku."},{"role":"assistant","content":"..."}]}
```

Use:

```bash
--input-key messages
```

Do not set `--apply-chat-template` with `slime.rollout.sft_rollout.generate_rollout`. The generic dataset loader would render the messages into a string, while `sft_rollout` expects `sample.prompt` to remain a list of message dictionaries so `MultiTurnLossMaskGenerator` can build the training loss mask.

## Per-Turn Loss Mask

For SFT, message entries can include `step_loss_mask`:

```json
{"messages":[
  {"role":"user","content":"Question","step_loss_mask":0},
  {"role":"assistant","content":"Answer","step_loss_mask":1}
]}
```

A `0` masks the turn from the loss; `1` contributes normally.

## Already Rendered Text

Already rendered text is not compatible with the stock `sft_rollout` loss-mask path because it needs per-message roles and optional `step_loss_mask`. Use message-list data for the stock SFT rollout, or write a custom rollout function that tokenizes rendered text and creates `Sample.tokens`, `Sample.response_length`, `Sample.reward`, and `Sample.loss_mask`.

## Parquet

slime examples include parquet datasets. The same logical keys apply; ensure the environment has dataset readers for the file format.
