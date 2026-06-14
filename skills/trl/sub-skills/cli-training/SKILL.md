---
name: cli-training
description: "Use the TRL command-line interface for SFT, DPO, GRPO, reward, RLOO, KTO, YAML config files, Accelerate launch flags, environment checks, and CLI troubleshooting."
---

# CLI Training

Use this sub-skill when a user wants to run TRL from the terminal, convert Python trainer usage to commands, write YAML training configs, or debug `trl` CLI arguments.

## Commands

The installed CLI entry point is `trl`. Current command groups include:

```bash
trl --help
trl env
trl sft --help
trl dpo --help
trl grpo --help
trl reward --help
trl rloo --help
trl kto --help
trl vllm-serve --help
trl skills --help
```

Use [references/cli-reference.md](references/cli-reference.md) for command recipes, YAML configs, and common flags.

## Basic Training Commands

SFT:

```bash
trl sft \
  --model_name_or_path Qwen/Qwen2.5-0.5B \
  --dataset_name trl-lib/Capybara \
  --output_dir Qwen2.5-0.5B-SFT
```

DPO:

```bash
trl dpo \
  --model_name_or_path Qwen/Qwen2.5-0.5B-Instruct \
  --dataset_name trl-lib/ultrafeedback_binarized \
  --output_dir Qwen2.5-0.5B-DPO
```

Reward model:

```bash
trl reward \
  --model_name_or_path Qwen/Qwen2.5-0.5B-Instruct \
  --dataset_name trl-lib/ultrafeedback_binarized \
  --output_dir Qwen2.5-0.5B-Reward
```

GRPO:

```bash
trl grpo \
  --model_name_or_path Qwen/Qwen2.5-0.5B-Instruct \
  --dataset_name trl-lib/DeepMath-103K \
  --reward_funcs accuracy_reward \
  --output_dir Qwen2.5-0.5B-GRPO
```

RLOO:

```bash
trl rloo \
  --model_name_or_path Qwen/Qwen2.5-0.5B-Instruct \
  --dataset_name trl-lib/DeepMath-103K \
  --reward_funcs accuracy_reward \
  --output_dir Qwen2.5-0.5B-RLOO
```

KTO:

```bash
trl kto \
  --model_name_or_path Qwen/Qwen2.5-0.5B-Instruct \
  --dataset_name trl-lib/kto-mix-14k \
  --output_dir Qwen2.5-0.5B-KTO
```

KTO emits an experimental warning in current TRL because it imports from `trl.experimental.kto`.

## YAML Configs

Prefer YAML config files for repeatable runs:

```yaml
model_name_or_path: Qwen/Qwen2.5-0.5B
dataset_name: trl-lib/Capybara
output_dir: Qwen2.5-0.5B-SFT
learning_rate: 2.0e-5
per_device_train_batch_size: 2
gradient_accumulation_steps: 8
num_train_epochs: 1
report_to: none
```

Launch:

```bash
trl sft --config sft_config.yaml
```

## Distributed CLI

TRL CLI accepts Accelerate-style launch options such as `--num_processes`. For complex setups, run scripts or CLI commands through `accelerate launch` and use an Accelerate config file.

```bash
trl sft \
  --config sft_config.yaml \
  --num_processes 4
```

For vLLM serving or generation acceleration, switch to [../vllm-and-distributed/SKILL.md](../vllm-and-distributed/SKILL.md).

## Debugging

1. Run `trl env` and `trl <command> --help`.
2. Confirm the dataset has the expected columns for the selected trainer.
3. Move long command lines into YAML to avoid quoting and shell-continuation mistakes.
4. Add output/logging/eval flags incrementally.
5. If a command fails on a trainer-specific flag, compare it against `trl <command> --help`; not every Python config option is usable under every CLI command.

For dataset schemas, use [../data-and-rewards/SKILL.md](../data-and-rewards/SKILL.md). For stable Python trainer APIs, use [../core-trainers/SKILL.md](../core-trainers/SKILL.md).
