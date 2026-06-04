---
name: slime-custom-rollout
description: "Guides agents through slime custom rollout, custom generate, reward model, filters, loss, data source, eval function, and Megatron hook interfaces."
disable-model-invocation: true
---

# slime Custom Rollout

Use this sub-skill when the user wants to customize data generation, reward computation, filtering, custom loss, custom data source, eval rollout, or Megatron hooks.

## Short Workflow

1. Choose the narrowest hook that solves the problem.
2. Start from root [../../scripts/minimal_custom_hooks.py](../../scripts/minimal_custom_hooks.py) and copy only the needed function into the user's project.
3. Wire it by import path, for example `--custom-generate-function-path mypkg.rollout.generate`.
4. Validate signatures before running a GPU job.
5. For agent/tool/RAG scenarios, route to `slime-agentic-tool-use` after selecting hooks.

Read [references/api-reference.md](references/api-reference.md) for verified function signatures and return types. Read [references/workflows.md](references/workflows.md) for hook selection. Read [references/troubleshooting.md](references/troubleshooting.md) when custom code fails contract tests or breaks training data shape.

## Scripts

- Read/adapt root [../../scripts/minimal_custom_hooks.py](../../scripts/minimal_custom_hooks.py).
- Adapt [scripts/validate_custom_hook_import.py](scripts/validate_custom_hook_import.py) to check a hook path import and signature.

## Hook Selection

- Replace only per-sample generation: `--custom-generate-function-path`.
- Replace whole rollout orchestration: `--rollout-function-path`.
- Add reward logic: `--custom-rm-path`.
- Filter sample groups during dynamic sampling: `--dynamic-sampling-filter-path`.
- Filter buffer before training: `--buffer-filter-path`.
- Mask individual samples: `--rollout-sample-filter-path`.
- Change training loss: `--loss-type custom_loss --custom-loss-function-path`.
- Override prompt source: `--data-source-path`.
- Override evaluation only: `--eval-function-path`.
