---
name: slime-fault-tolerance-reproducibility
description: "Configures slime rollout health checks, fault tolerance, deterministic inference/training, resume behavior, and reproducibility-oriented runtime variables."
disable-model-invocation: true
---

# slime Fault Tolerance Reproducibility

Use this sub-skill for long-running jobs, rollout health checks, deterministic experiments, resume behavior, or production stability settings.

## Short Workflow

1. Enable fault tolerance for production rollout jobs.
2. Increase first health-check wait for large MoE or kernel-compile-heavy models.
3. Save checkpoints regularly and resume by setting `--load` equal to `--save`.
4. For reproducibility, enable deterministic SGLang and Megatron settings and runtime env vars.
5. Use root troubleshooting for checkpoint and stop-token issues.

Read [references/configuration.md](references/configuration.md) for fault-tolerance and deterministic flags. Read [references/troubleshooting.md](references/troubleshooting.md) for resume and health-check issues.

## Scripts

- Adapt [scripts/fault_tolerance_args.sh](scripts/fault_tolerance_args.sh) and [scripts/deterministic_runtime_env.json](scripts/deterministic_runtime_env.json).
