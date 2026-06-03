---
name: slime-evaluation
description: "Configures slime periodic evaluation, --eval-prompt-data, structured --eval-config, multi-task eval, custom eval rollout, and per-dataset reward overrides."
disable-model-invocation: true
---

# slime Evaluation

Use this sub-skill when adding periodic eval, multiple eval datasets, eval-specific sampling, or custom evaluation functions.

## Short Workflow

1. For one dataset, use `--eval-prompt-data name path`.
2. For multiple datasets or per-dataset overrides, write `--eval-config` YAML.
3. Set `--eval-interval`.
4. Override eval sampling with `--n-samples-per-eval-prompt`, `--eval-max-response-len`, `--eval-top-p`, etc.
5. Use `--eval-function-path` only when eval generation differs structurally from training rollout.

Read [references/configuration.md](references/configuration.md) for CLI and YAML forms. Read [references/troubleshooting.md](references/troubleshooting.md) for missing dataset or reward-key issues.

## Scripts

- Adapt [scripts/multi_task_eval.yaml](scripts/multi_task_eval.yaml) and [scripts/eval_args.sh](scripts/eval_args.sh).
