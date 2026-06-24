# RL Data Formats

slime prompt datasets are JSONL: one JSON object per line.

## Chat-Template Prompt Example

```json
{"prompt":[{"role":"user","content":"Solve: 1+1. Answer with a number."}],"label":"2"}
```

Use:

```bash
--prompt-data train.jsonl
--input-key prompt
--label-key label
--apply-chat-template
```

## Plain Prompt Example

```json
{"input":"Solve: 1+1. Answer with a number.","label":"2"}
```

Use:

```bash
--input-key input
--label-key label
```

## Metadata

Custom rollout, reward, sandbox, RAG, and tool-use flows often use:

```json
{"prompt":"...", "label":"...", "metadata":{"task_id":"abc"}}
```

Default metadata key is `metadata`; override with `--metadata-key`.

## SFT Loss Mask Field

For chat-message prompts used in SFT, a message can include `step_loss_mask`. A value of `0` masks that turn from loss; `1` contributes to the normal loss mask.
