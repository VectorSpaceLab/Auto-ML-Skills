# Install And Environment

Read this when setting up TRL, selecting extras, checking imports, or debugging package/backend failures.

## Public Install Paths

Normal user install:

```bash
pip install trl
```

Latest source install:

```bash
pip install git+https://github.com/huggingface/trl.git
```

Editable development install from a checkout:

```bash
pip install -e .
pip install -e ".[dev]"
```

TRL declares Python `>=3.10` and depends on `accelerate`, `datasets`, `jinja2`, `packaging`, and `transformers`. The package entry point is `trl = trl.cli:main`.

## Extras

Use only the extras needed for the task:

| Extra | Use |
| --- | --- |
| `trl[peft]` | LoRA/PEFT adapters through `peft_config` or CLI `--use_peft` |
| `trl[vllm]` | `trl vllm-serve`, GRPO/RLOO vLLM generation, server or colocate mode |
| `trl[vlm]` | Vision-language model and multimodal message workflows |
| `trl[deepspeed]` | DeepSpeed integration |
| `trl[liger]` | Liger kernels |
| `trl[quantization]` | `bitsandbytes` quantization paths |
| `trl[openreward]` | OpenReward integration on Python 3.11+ |
| `trl[test]` | Test dependencies |

Avoid installing every extra by default. `vllm`, `deepspeed`, `bitsandbytes`, and kernel packages are sensitive to Python version, CUDA support, GPU architecture, and compiler/toolkit availability.

## Minimal Verification

```bash
python - <<'PY'
import importlib.metadata as md
import trl
from trl import SFTTrainer, DPOTrainer, GRPOTrainer, RewardTrainer, RLOOTrainer
print("trl", md.version("trl"))
print(SFTTrainer.__name__, DPOTrainer.__name__, GRPOTrainer.__name__, RewardTrainer.__name__, RLOOTrainer.__name__)
PY
python -m pip check
trl --help
```

The stable root namespace includes:

- Trainers/configs: `SFTTrainer`, `SFTConfig`, `DPOTrainer`, `DPOConfig`, `GRPOTrainer`, `GRPOConfig`, `RewardTrainer`, `RewardConfig`, `RLOOTrainer`, `RLOOConfig`, `KTOTrainer`, `KTOConfig`.
- Utilities: `apply_chat_template`, `maybe_apply_chat_template`, `pack_dataset`, `unpair_preference_dataset`, `create_reference_model`, `TrlParser`, `ScriptArguments`, `ModelConfig`.

Some algorithms have documentation under `trl.experimental`. Treat that namespace as unstable and check current imports before writing code against it.

## Backend Checks

For CPU/API inspection, importing TRL and trainer classes is enough. For GPU training claims, also check the selected framework:

```bash
python - <<'PY'
import torch
print(torch.__version__, torch.version.cuda)
print("cuda available", torch.cuda.is_available(), "devices", torch.cuda.device_count())
if torch.cuda.is_available():
    print(torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0))
    torch.empty((1,), device="cuda")
PY
```

For vLLM workflows, verify:

```bash
python -c "import vllm; print(vllm.__version__)"
trl vllm-serve --help
```

Do not claim vLLM support from `trl` import success alone. vLLM has separate package and hardware requirements.

## Common Failures

`ModuleNotFoundError: peft`:
Install `trl[peft]` or `peft`, then retry. Python trainer APIs accept `peft_config`; CLI workflows use flags such as `--use_peft`, `--lora_r`, and `--lora_alpha`.

`ModuleNotFoundError: vllm`:
Install `trl[vllm]` and verify the CUDA/Python compatibility of the installed vLLM wheel. vLLM paths are used by `trl vllm-serve` and by GRPO/RLOO configs such as `use_vllm=True`.

Out of memory during training:
Start by reducing `per_device_train_batch_size`, increasing `gradient_accumulation_steps`, lowering sequence lengths (`max_length` or `max_completion_length`), disabling large eval batches, and enabling `gradient_checkpointing`. Then consider PEFT/LoRA, quantization, Liger kernels, FSDP, or DeepSpeed.

Chat template or assistant-only loss issues:
For SFT `assistant_only_loss=True`, the chat template must support generation masks. TRL ships patched training templates for several model families; use `chat_template_path` or `get_training_chat_template` when needed.

Unexpected experimental import warning:
Imports from `trl.experimental` intentionally warn that APIs are unstable. Do not silence this warning in generated user code unless the user explicitly accepts experimental risk.
