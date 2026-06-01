---
name: trl-cli-and-scripts
description: Use TRL command-line training commands, YAML configs, TrlParser, script utilities, and packaged skills commands.
license: Apache-2.0
---

# TRL CLI And Scripts

Use this sub-skill when the task asks for terminal commands, YAML config files, `trl` CLI usage, script argument parsing, `TrlParser`, dataset mixtures, or reusable launch recipes.

## Commands

The inspected TRL CLI exposes:

- `trl sft`
- `trl dpo`
- `trl grpo`
- `trl kto`
- `trl reward`
- `trl rloo`
- `trl env`
- `trl skills`
- `trl vllm-serve`

Run [scripts/print_cli_summary.py](scripts/print_cli_summary.py) in the target environment to confirm commands and show concise help.

## Basic CLI Pattern

```bash
trl sft \
  --model_name_or_path Qwen/Qwen2.5-0.5B \
  --dataset_name trl-lib/Capybara \
  --output_dir Qwen2.5-0.5B-SFT
```

```bash
trl dpo \
  --model_name_or_path Qwen/Qwen2.5-0.5B-Instruct \
  --dataset_name trl-lib/ultrafeedback_binarized \
  --output_dir Qwen2.5-0.5B-DPO
```

```bash
trl grpo \
  --model_name_or_path Qwen/Qwen2.5-0.5B-Instruct \
  --dataset_name trl-lib/DeepMath-103K \
  --reward_funcs accuracy_reward \
  --output_dir Qwen2.5-0.5B-GRPO
```

Read [references/cli-reference.md](references/cli-reference.md) for command details and [references/configuration.md](references/configuration.md) for YAML patterns.

## YAML Config Pattern

Any training command can load a config:

```bash
trl sft --config sft_config.yaml
```

Generate a starter config with [scripts/make_trl_config.py](scripts/make_trl_config.py):

```bash
python scripts/make_trl_config.py sft --model Qwen/Qwen2.5-0.5B --dataset trl-lib/Capybara
```

## Accelerate Behavior

Training commands are CLI wrappers around `trl.scripts.<command>` modules. The CLI parses script/config args, resolves Accelerate launch args, then launches the training script. You can pass Accelerate-related arguments such as `--num_processes` through the `trl` command.

For more complex distributed launch recipes, use [scaling-integrations](../scaling-integrations/SKILL.md).

## Script Utilities

TRL exposes script-facing objects:

- `ScriptArguments`
- `DatasetConfig`
- `DatasetMixtureConfig`
- `TrlParser`
- `get_dataset`
- `init_zero_verbose`

Use them when building scripts that should accept the same config and dataset arguments as official TRL scripts.

## References

- [references/cli-reference.md](references/cli-reference.md): Command list, common flags, and vLLM/skills command notes.
- [references/configuration.md](references/configuration.md): YAML config, dataset mixtures, `TrlParser`, and script-building patterns.
- [references/troubleshooting.md](references/troubleshooting.md): CLI parsing, config, Accelerate, and command discovery failures.
