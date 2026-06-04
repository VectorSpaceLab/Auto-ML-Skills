---
name: slime-ppo-megatron-config
description: "Configures slime PPO actor and critic resources, critic warmup, and role-specific Megatron overrides through --megatron-config-path."
disable-model-invocation: true
---

# slime PPO Megatron Config

Use this sub-skill when `--advantage-estimator ppo` or critic training is requested.

## Short Workflow

1. Start from `slime-rl-training`.
2. Add PPO objective flags and critic resources.
3. If actor and critic need different load/save/lr values, write `--megatron-config-path`.
4. Keep actor and critic Megatron parallel topology aligned; YAML is for role overrides, not GPU placement.

Read [references/configuration.md](references/configuration.md) for YAML schema and PPO args. Read [references/troubleshooting.md](references/troubleshooting.md) for actor/critic resource and override mistakes.

## Scripts

- Adapt [scripts/megatron_ppo.yaml](scripts/megatron_ppo.yaml) and [scripts/ppo_args.sh](scripts/ppo_args.sh).

## Constraints

- `--megatron-config-path` is mainly intended for PPO actor/critic role overrides.
- Placement still uses CLI resource flags such as `--actor-num-*` and `--critic-num-*`.
- In current PPO, actor and critic should keep the same Megatron parallel topology.
