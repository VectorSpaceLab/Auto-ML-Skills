---
name: slime-pd-disaggregation
description: "Configures slime prefill/decode disaggregation for long-context, multi-turn, and agentic SGLang rollout workloads."
disable-model-invocation: true
---

# slime PD Disaggregation

Use this sub-skill when a user wants Prefill/Decode disaggregation, separate prefill and decode capacity, or long-context/agentic rollout performance tuning.

## Short Workflow

1. For quick experiments, use legacy `--prefill-num-servers`.
2. For new or complex deployments, use `--sglang-config` with `prefill` and `decode` server groups.
3. Keep total YAML GPUs equal to `--rollout-num-gpus`.
4. Validate YAML before submitting the Ray job.

Read [references/workflows.md](references/workflows.md) for the two configuration paths. Read [references/troubleshooting.md](references/troubleshooting.md) when topology validation or startup fails.

## Scripts

- Adapt [scripts/sglang_pd.yaml](scripts/sglang_pd.yaml) or [scripts/sglang_multi_model_pd.yaml](scripts/sglang_multi_model_pd.yaml).
- Validate with root [../../scripts/validate_sglang_config.py](../../scripts/validate_sglang_config.py).

## Handoff

Route back to `slime-sglang-deployment` for general SGLang/router flags, and to `slime-agentic-tool-use` when PD is supporting a tool or multi-turn rollout.
