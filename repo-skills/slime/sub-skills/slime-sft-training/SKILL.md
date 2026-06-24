---
name: slime-sft-training
description: "Builds slime supervised fine-tuning workflows using sft_rollout, sft_loss, debug-train-only, Ray launch, and Megatron checkpoints."
disable-model-invocation: true
---

# slime SFT Training

Use this sub-skill when the user wants supervised fine-tuning rather than RL. In slime, SFT is configured through the training pipeline with `sft_rollout` and `sft_loss`; it is not a separate CLI.

## Short Workflow

1. Verify environment and Megatron imports with `slime-environment-setup`.
2. If `REF_LOAD` does not already point to a valid Megatron checkpoint root, convert HF checkpoint to Megatron `torch_dist` with `slime-checkpoint-conversion`.
3. Select model args with `slime-model-recipes`.
4. Prepare SFT JSONL/parquet data with message or tokenizable text fields.
5. Use:
   - `--rollout-function-path slime.rollout.sft_rollout.generate_rollout`
   - `--loss-type sft_loss`
   - `--calculate-per-token-loss`
   - `--disable-compute-advantages-and-returns`
   - commonly `--debug-train-only`
6. Submit through [../../scripts/run_slime_train_async.py](../../scripts/run_slime_train_async.py) unless the user needs the synchronous driver.

Read [references/workflows.md](references/workflows.md) for SFT launch recipes. Read [references/data-formats.md](references/data-formats.md) for loss mask and message data. Read [references/troubleshooting.md](references/troubleshooting.md) for common SFT issues.

## Scripts

- Adapt [scripts/run_sft_template.sh](scripts/run_sft_template.sh) for a small SFT run.

## Decision Points

- For `slime.rollout.sft_rollout.generate_rollout`, pass OpenAI-style message lists directly and do not set `--apply-chat-template`; the SFT rollout builds the loss mask from message dictionaries.
- Use `step_loss_mask` inside messages when some turns should not contribute to loss.
- If using async driver, do not set `--colocate`.
- For multimodal SFT, route to `slime-vlm-training`.
