---
name: slime-vlm-training
description: "Builds slime multimodal and VLM SFT/RL workflows with image data, multimodal keys, Megatron Bridge caveats, and GEO3K-style examples."
disable-model-invocation: true
---

# slime VLM Training

Use this sub-skill when the user wants multimodal/VLM training, image-based prompts, GEO3K-style tasks, or Qwen-VL/Qwen3-VL model support.

## Short Workflow

1. Confirm the model backend supports the VLM architecture and required bridge/plugin.
2. Prepare data with text fields plus image keys.
3. Set `--multimodal-keys` JSON to map media types to data keys.
4. Use SFT or RL training skill depending on objective.
5. For multi-turn VLM environments, use `slime-agentic-tool-use` and `slime-custom-rollout`.

Read [references/workflows.md](references/workflows.md) for single-turn and multi-turn VLM patterns. Read [references/data-formats.md](references/data-formats.md) for multimodal dataset keys. Read [references/troubleshooting.md](references/troubleshooting.md) for backend caveats.

## Scripts

- Adapt [scripts/vlm_args.sh](scripts/vlm_args.sh).
