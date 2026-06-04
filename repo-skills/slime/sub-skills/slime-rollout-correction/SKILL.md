---
name: slime-rollout-correction
description: "Configures slime train-inference mismatch monitoring, rollout logprob bypass, TIS/MIS correction, and custom importance sampling hooks."
disable-model-invocation: true
---

# slime Rollout Correction

Use this sub-skill when the user asks for TIS, MIS, rollout correction, rollout logprob reuse, train-inference mismatch metrics, or off-policy sequence masking.

## Short Workflow

1. Decide if the user only wants metrics or wants loss correction.
2. For metrics only, use `--get-mismatch-metrics`.
3. For rollout logprob bypass, use `--use-rollout-logprobs`.
4. For correction, use `--use-tis` and optionally `--custom-tis-function-path`.
5. Ensure rollout generation collects logprobs when correction depends on rollout policy probabilities.

Read [references/configuration.md](references/configuration.md) for algorithms and flags. Read [references/troubleshooting.md](references/troubleshooting.md) for missing logprob and high-variance correction problems.

## Scripts

- Adapt [scripts/tis_args.sh](scripts/tis_args.sh) and [scripts/mis_config.yaml](scripts/mis_config.yaml).
