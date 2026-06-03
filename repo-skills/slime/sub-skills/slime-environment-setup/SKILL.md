---
name: slime-environment-setup
description: "Guides agents through slime Docker or source setup, Ray launch, runtime environment checks, and training entrypoint selection."
disable-model-invocation: true
---

# slime Environment Setup

Use this sub-skill when the user asks to install slime, create an environment, start Ray, repair imports, or prepare a launch shell before choosing RL/SFT/eval details.

## Short Workflow

1. Choose Docker unless the user explicitly needs custom source patches.
2. Verify `import slime` and `import slime_plugins`.
3. Verify strict training imports if a training job will run: full Megatron-LM must be on `PYTHONPATH`.
4. Start Ray head only after GPU count and colocate/decoupled resource math are known.
5. Launch through a bundled runner:
   - root [../../scripts/run_slime_train.py](../../scripts/run_slime_train.py) for normal synchronous training.
   - root [../../scripts/run_slime_train_async.py](../../scripts/run_slime_train_async.py) for async training or SFT recipes that use data prefetch.

Read [references/workflows.md](references/workflows.md) for Docker/source setup, Ray startup, and runtime-env JSON patterns. Read [references/configuration.md](references/configuration.md) for environment variables and resource math. Read [references/troubleshooting.md](references/troubleshooting.md) when imports, Ray job submission, or process cleanup fail.

## Scripts

- Run root [../../scripts/check_env.py](../../scripts/check_env.py) before any training launch. Use `--strict-train` when Megatron-backed parsing must work.
- Adapt [scripts/start_ray_head.sh](scripts/start_ray_head.sh) to start a local Ray head safely.
- Adapt root [../../scripts/launch_ray_job_template.sh](../../scripts/launch_ray_job_template.sh) to submit a slime job with a runtime env.

## Decision Points

- If the user only wants to inspect APIs or build data/hook code, non-strict import verification is enough.
- If the user wants RL, SFT, checkpoint conversion, or any `train.py` equivalent, strict Megatron verification is required.
- If the job is colocated, `--colocate` means rollout and actor share actor GPUs; do not also count `--rollout-num-gpus`.
- If the job is decoupled, total GPUs must cover actor plus rollout, and PPO may add critic GPUs.
- If the user asks for a clean rerun, stop Ray/SGLang only after checking no other job is using the node.

## Handoff

After environment setup:

- Use `slime-checkpoint-conversion` if the user has only Hugging Face weights.
- Use `slime-model-recipes` to select Megatron model args.
- Use `slime-rl-training` or `slime-sft-training` to assemble the final job.
