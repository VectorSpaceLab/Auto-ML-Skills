---
name: slime-rl-training
description: "Builds standard slime RL training pipelines with Megatron actors, SGLang rollout, GRPO, GSPO, REINFORCE++, PPO-like objectives, Ray launch, and evaluation hooks."
disable-model-invocation: true
---

# slime RL Training

Use this sub-skill for ordinary slime reinforcement learning jobs: rollout with SGLang, reward calculation, Megatron train step, weight sync back to rollout, and optional evaluation.

## Short Workflow

1. Verify environment with `slime-environment-setup`.
2. If `REF_LOAD` does not already point to a valid Megatron checkpoint root, convert HF weights to Megatron `torch_dist` with `slime-checkpoint-conversion`.
3. Select model args with `slime-model-recipes`.
4. Prepare JSONL prompt data with `input_key`, `label_key`, and optional `metadata_key`.
5. Assemble args blocks: checkpoint, rollout, eval, performance, algorithm, optimizer, SGLang.
6. Submit through Ray using root [../../scripts/run_slime_train.py](../../scripts/run_slime_train.py).

Read [references/workflows.md](references/workflows.md) for end-to-end RL launch recipes. Read [references/configuration.md](references/configuration.md) for argument blocks and batch-size constraints. Read [references/data-formats.md](references/data-formats.md) for prompt JSONL requirements. Read [references/troubleshooting.md](references/troubleshooting.md) for common launch/runtime failures.

## Scripts

- Adapt [scripts/run_grpo_template.sh](scripts/run_grpo_template.sh) for a single-node GRPO-style job.
- Use root [../../scripts/launch_ray_job_template.sh](../../scripts/launch_ray_job_template.sh) if you prefer passing args from another script.

## Decision Points

- Use `grpo` for critic-free grouped rewards.
- Use `ppo` when value-function critic training is required; route to `slime-ppo-megatron-config`.
- Use `--use-kl-loss` for KL loss monitoring or regularization; `--kl-loss-coef 0` only logs.
- Keep `(rollout_batch_size * n_samples_per_prompt) == (global_batch_size * num_steps_per_rollout)` unless relying on slime's automatic calculation.
- Use `--balance-data` and dynamic batching for variable-length samples.

## Related Sub-Skills

- `slime-agentic-tool-use` for tool/RAG/sandbox rollout.
- `slime-sglang-deployment` for advanced SGLang topology.
- `slime-evaluation` for periodic or multi-task eval.
- `slime-debug-trace-profile` for rollout-only or train-only isolation.
