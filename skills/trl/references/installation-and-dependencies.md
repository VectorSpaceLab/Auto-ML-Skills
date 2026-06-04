# Installation And Dependencies

Read this when setting up TRL or diagnosing import and optional-backend problems.

## Core Package

TRL requires Python 3.10 or newer. Its core dependencies are:

- `accelerate`
- `datasets`
- `jinja2`
- `packaging`
- `transformers`

Install from PyPI:

```bash
pip install trl
```

Install the latest public source:

```bash
pip install "git+https://github.com/huggingface/trl.git"
```

Install for TRL source development:

```bash
git clone https://github.com/huggingface/trl.git
cd trl
pip install -e ".[dev]"
```

## Optional Extras

Use extras only for workflows that need them:

| Extra | Install | Use when |
| --- | --- | --- |
| `peft` | `pip install "trl[peft]"` | LoRA, QLoRA, adapters, PEFT configs |
| `quantization` | `pip install "trl[quantization]"` | bitsandbytes 4-bit or 8-bit loading |
| `vllm` | `pip install "trl[vllm]"` | vLLM-backed generation or `trl vllm-serve` |
| `liger` | `pip install "trl[liger]"` | `use_liger_kernel=True` |
| `kernels` | `pip install "trl[kernels]"` | Hub-hosted optimized kernels through Transformers |
| `deepspeed` | `pip install "trl[deepspeed]"` | DeepSpeed ZeRO launch configs |
| `vlm` | `pip install "trl[vlm]"` | vision-language examples and image/video preprocessing |
| `math_verify` | `pip install "trl[math_verify]"` | math/reasoning reward verification helpers |
| `openreward` | `pip install "trl[openreward]"` | experimental OpenReward environment integration |

The `dev` extra is broad but intentionally does not include vLLM by default in the inspected package metadata because vLLM can be CUDA-sensitive.

## Minimal Import Check

```bash
python - <<'PY'
import trl
print("trl", trl.__version__)
from trl import SFTTrainer, DPOTrainer, GRPOTrainer, RLOOTrainer, RewardTrainer
from trl import SFTConfig, DPOConfig, GRPOConfig, RLOOConfig, RewardConfig
print("stable trainers import")
PY
```

For a reusable version, run [../scripts/check_env.py](../scripts/check_env.py).

## CLI Check

```bash
trl --help
trl env
```

Expected top-level CLI commands in the inspected v1-style package:

- `trl dpo`
- `trl env`
- `trl grpo`
- `trl kto`
- `trl reward`
- `trl rloo`
- `trl sft`
- `trl skills`
- `trl vllm-serve`

## Public API Families

Stable top-level imports include:

- Trainers/configs: `SFTTrainer`, `SFTConfig`, `DPOTrainer`, `DPOConfig`, `GRPOTrainer`, `GRPOConfig`, `RLOOTrainer`, `RLOOConfig`, `RewardTrainer`, `RewardConfig`.
- Model/script configs: `ModelConfig`, `ScriptArguments`, `DatasetMixtureConfig`, `TrlParser`, `get_dataset`.
- Data helpers: `is_conversational`, `apply_chat_template`, `maybe_apply_chat_template`, `maybe_convert_to_chatml`, `extract_prompt`, `maybe_extract_prompt`, `unpair_preference_dataset`, `maybe_unpair_preference_dataset`, `pack_dataset`, `prepare_multimodal_messages`, `prepare_multimodal_messages_vllm`.
- Chat-template helpers: `get_training_chat_template`, `clone_chat_template`, `supports_tool_calling`.
- Model helpers: `create_reference_model`, `get_quantization_config`, `get_kbit_device_map`, `get_peft_config`.
- Reward functions under `trl.rewards`: `accuracy_reward`, `reasoning_accuracy_reward`, `think_format_reward`, `get_soft_overlong_punishment`.

KTO may be visible at top level in some installs, but the docs classify KTO as experimental in TRL v1. Prefer checking the installed package and warning about stability.

## Version-Sensitive Checks

When exact behavior matters, verify the installed package instead of relying on this static skill:

```bash
python scripts/inspect_public_api.py --objects SFTTrainer SFTConfig GRPOConfig
trl sft --help
```

For vLLM, verify the installed vLLM version and TRL compatibility. The inspected docs support vLLM versions from `0.12.0` through `0.19.0`.
