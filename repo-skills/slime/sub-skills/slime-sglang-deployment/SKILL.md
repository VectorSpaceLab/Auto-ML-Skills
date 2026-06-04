---
name: slime-sglang-deployment
description: "Configures slime SGLang rollout engines, router flags, external engines, multi-model serving, and --sglang-config YAML topologies."
disable-model-invocation: true
---

# slime SGLang Deployment

Use this sub-skill when the user asks about rollout engine resources, SGLang flags, router behavior, `--sglang-config`, multi-model serving, external engines, or SGLang topology validation.

## Short Workflow

1. Decide whether slime manages SGLang engines or connects to external engines.
2. For the default managed path, set `--rollout-num-gpus` and `--rollout-num-gpus-per-engine`; pass SGLang server flags as `--sglang-*`.
3. For router behavior, pass router flags as `--router-*`.
4. For multi-model serving, heterogeneous groups, placeholder reservations, or PD topology, write `--sglang-config` YAML.
5. Validate YAML with root [../../scripts/validate_sglang_config.py](../../scripts/validate_sglang_config.py) before launch.

Read [references/configuration.md](references/configuration.md) for default SGLang and router flags. Read [references/sglang-config.md](references/sglang-config.md) for YAML schema and examples. Read [references/troubleshooting.md](references/troubleshooting.md) for startup and memory failures.

## Scripts

- Validate YAML with root [../../scripts/validate_sglang_config.py](../../scripts/validate_sglang_config.py).
- Adapt [scripts/sglang_basic.yaml](scripts/sglang_basic.yaml), [scripts/sglang_multi_model.yaml](scripts/sglang_multi_model.yaml), or [scripts/sglang_external_args.sh](scripts/sglang_external_args.sh).

## Constraints

- `--sglang-config` is mutually exclusive with `--rollout-external`.
- `--sglang-config` is mutually exclusive with legacy `--prefill-num-servers`.
- In YAML, total `server_groups[*].num_gpus` across all models must equal `--rollout-num-gpus`.
- `--rollout-num-gpus-per-engine` maps to SGLang TP size unless overridden by YAML group settings.
