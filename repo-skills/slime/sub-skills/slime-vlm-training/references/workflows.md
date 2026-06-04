# VLM Workflows

## Single-Turn VLM RL

Use standard RL training with multimodal data:

```bash
--prompt-data /data/geo3k.jsonl
--input-key messages
--label-key answer
--multimodal-keys '{"image":"images"}'
--apply-chat-template
--rm-type deepscaler
```

## VLM SFT

Use `slime-sft-training` with:

```bash
--rollout-function-path slime.rollout.sft_rollout.generate_rollout
--loss-type sft_loss
--multimodal-keys '{"image":"images"}'
```

## Multi-Turn VLM

Use a custom generate or full rollout function that owns the environment state and image observations.

```bash
--custom-generate-function-path my_vlm_env.generate
--custom-rm-path my_vlm_env.reward
```
