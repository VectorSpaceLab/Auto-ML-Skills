# Configuration And Script Utilities

Read this when using YAML configs, creating reusable TRL scripts, or loading dataset mixtures.

## YAML Configs

Training CLI commands accept config files:

```bash
trl sft --config sft_config.yaml
```

Minimal SFT config:

```yaml
model_name_or_path: Qwen/Qwen2.5-0.5B
dataset_name: trl-lib/Capybara
output_dir: sft-output
learning_rate: 2.0e-5
max_length: 1024
per_device_train_batch_size: 2
gradient_accumulation_steps: 8
```

Minimal DPO config:

```yaml
model_name_or_path: Qwen/Qwen3-0.6B
dataset_name: trl-lib/ultrafeedback_binarized
output_dir: dpo-output
learning_rate: 1.0e-6
beta: 0.1
per_device_train_batch_size: 2
gradient_accumulation_steps: 8
```

Minimal GRPO config:

```yaml
model_name_or_path: Qwen/Qwen2.5-0.5B-Instruct
dataset_name: trl-lib/DeepMath-103K
reward_funcs:
  - accuracy_reward
output_dir: grpo-output
num_generations: 8
max_completion_length: 256
```

Use [../scripts/make_trl_config.py](../scripts/make_trl_config.py) to generate starter YAML.

## Dataset Mixtures

`DatasetMixtureConfig` supports a list of dataset configs:

```yaml
datasets:
  - path: trl-lib/Capybara
    split: train
    columns:
      - messages
  - path: my-org/my-dataset
    name: default
    split: train
streaming: false
test_split_size: 0.05
```

Fields for each dataset:

- `path`
- `name`
- `data_dir`
- `data_files`
- `split`
- `columns`

If `datasets` is provided, single-dataset fields such as `dataset_name` are ignored by TRL script utilities.

## `ScriptArguments`

Common dataset script args:

```python
from trl import ScriptArguments
```

Fields:

- `dataset_name`
- `dataset_config`
- `dataset_train_split`
- `dataset_test_split`
- `dataset_streaming`
- `ignore_bias_buffers`

## `TrlParser`

Use `TrlParser` for scripts that should accept both CLI args and config files:

```python
from trl import ModelConfig, ScriptArguments, SFTConfig, TrlParser

parser = TrlParser((ScriptArguments, SFTConfig, ModelConfig))
script_args, training_args, model_args = parser.parse_args_and_config()
```

It extends a dataclass-backed argument parser and supports config-file loading. TRL CLI commands use the same style for official scripts.

## `get_dataset`

Use `get_dataset` to load train/eval datasets from `ScriptArguments` and `DatasetMixtureConfig` in official-script style:

```python
from trl import DatasetMixtureConfig, ScriptArguments, get_dataset

script_args = ScriptArguments(dataset_name="trl-lib/Capybara")
dataset_args = DatasetMixtureConfig()
dataset = get_dataset(script_args, dataset_args)
```

Inspect the installed signature before writing version-sensitive script code.

## `init_zero_verbose`

Use `init_zero_verbose()` near the top of CLI modules when clean script logging is needed before imports that can emit many warnings:

```python
from trl import init_zero_verbose

init_zero_verbose()
```

## CLI Command Internals

In the inspected source:

- Training commands import `trl.scripts.<name>`.
- Each script must expose `make_parser()`.
- The command parses config and CLI args separately enough to resolve Accelerate launch args.
- The command launches the training script through an Accelerate launcher.

This means CLI behavior can differ from calling `python -m trl.scripts.sft` directly. Prefer `trl <command>` for user-facing examples unless you specifically need script internals.
