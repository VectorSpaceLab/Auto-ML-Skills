---
name: peft
description: "Use this skill when working with Hugging Face PEFT: parameter-efficient finetuning, adapter configs, LoRA or prompt methods, adapter loading, quantization, merging, custom PEFT modules, and PEFT repository contributions."
---

# PEFT

Use this skill for Hugging Face PEFT work: configuring parameter-efficient adapters, wrapping base models, training and saving adapters, loading adapters for inference, composing or merging adapters, using quantized models, debugging adapter state, and contributing PEFT code.

PEFT is a Python package distributed as `peft`. Public imports come from `peft`.

## Start Here

For ordinary usage:

```bash
python -m pip install -U peft transformers accelerate torch safetensors
```

For local source work:

```bash
python -m pip install -e ".[test]"
```

Minimal verification:

```bash
python - <<'PY'
import peft
from peft import LoraConfig, TaskType, get_peft_model
print(peft.__version__)
print(LoraConfig(task_type=TaskType.CAUSAL_LM, r=8).__class__.__name__)
print(callable(get_peft_model))
PY
```

When changing PEFT itself, support Python `3.10`, `3.11`, `3.12`, and `3.13` based on the inspected repository test matrix.

## Route By Task

Read `sub-skills/adapter-training/SKILL.md` when the user wants to train or configure a PEFT method such as LoRA, AdaLoRA, IA3, prompt tuning, prefix tuning, LoHa, LoKr, BOFT, DoRA, trainable tokens, or task-specific adapters. This sub-skill covers config selection, `get_peft_model`, target modules, Trainer/custom-loop integration, and saving adapters.

Read `sub-skills/adapter-loading-and-composition/SKILL.md` when the user wants to load a trained adapter, use `AutoPeftModel*`, attach multiple adapters, switch adapters, merge or unload adapters, inspect adapter state, convert/check checkpoints, or debug bad inference after loading.

Read `sub-skills/quantization-and-optimization/SKILL.md` when the user mentions QLoRA, bitsandbytes, GPTQ, AQLM, EETQ, HQQ, torchao, INC, LoftQ, quantized training, adapter dtypes, `torch.compile`, low-memory loading, or accelerator-specific behavior.

Read `sub-skills/custom-peft-development/SKILL.md` when the user is applying PEFT to a non-Transformers model, using low-level adapter injection, adding a new PEFT method, extending supported model mappings, writing tests, or preparing a PEFT PR.

Read `references/api-reference.md` for verified public signatures, config classes, task types, adapter types, and method compatibility.

Read `references/troubleshooting.md` for common PEFT failures: wrong loading path, missing `modules_to_save`, added-token embeddings, dtype/AMP errors, repeated wrapping warnings, target-module misses, irregular adapter state, quantized merge limits, and contribution-policy pitfalls.

Run `scripts/check_peft_environment.py` to verify the installed package, dependency consistency, public imports, optional CUDA visibility, and core PEFT symbols in a user's Python environment.

## Core Workflow

Most PEFT tasks follow this shape:

```python
from peft import LoraConfig, TaskType, get_peft_model
from transformers import AutoModelForCausalLM

base_model = AutoModelForCausalLM.from_pretrained("model-id")
config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
)
model = get_peft_model(base_model, config)
model.print_trainable_parameters()
```

Train with Transformers `Trainer`, Accelerate, or a custom PyTorch loop. Save only the adapter:

```python
model.save_pretrained("adapter-output")
```

Load a trained adapter for inference by loading the compatible base model first, then loading the adapter:

```python
from peft import PeftConfig, PeftModel
from transformers import AutoModelForCausalLM

adapter_id = "namespace/model-adapter"
config = PeftConfig.from_pretrained(adapter_id)
base_model = AutoModelForCausalLM.from_pretrained(config.base_model_name_or_path)
model = PeftModel.from_pretrained(base_model, adapter_id)
model.eval()
```

Do not use `get_peft_model` to load trained adapter weights. `get_peft_model` creates a newly initialized PEFT wrapper for training.

## Contribution Guardrails

When working on `huggingface/peft`, follow the repository contribution policy before coding. AI-assisted contribution guideline breaches can result in automatic banning.

Human submitters must understand and defend every changed line. Before a PR, check overlapping issues/PRs, get maintainer approval for existing issues or new features, avoid tiny busywork PRs, run relevant tests, and state AI assistance in the PR description. If preparing a real upstream PR, verify the current upstream contribution guide and issue/PR state because repository policy can change.

Use `make style` for formatting/linting and select tests narrowly enough that at least one test runs. For example:

```bash
pytest tests/ -k "lora and not adalora and not randlora"
```

For bug fixes, write the failing regression test first, then implement the fix, then rerun the focused tests.
