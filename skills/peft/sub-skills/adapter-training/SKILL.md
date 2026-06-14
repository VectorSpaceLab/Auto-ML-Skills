---
name: adapter-training
description: "Use this sub-skill for configuring and training PEFT adapters, including LoRA, AdaLoRA, IA3, prompt tuning, prefix tuning, target modules, trainable tokens, Trainer loops, and saving adapters."
---

# Adapter Training

Use this sub-skill when a user wants to build a trainable PEFT model, choose an adapter method, configure `target_modules`, integrate with Transformers `Trainer` or a custom loop, save an adapter, or debug trainable-parameter counts.

Read `references/method-selection.md` to choose between LoRA variants, IA3, prompt methods, and other adapter configs.

Read `references/workflows.md` for practical training recipes, including LoRA, prompt/prefix methods, IA3, custom target modules, saving adapters, and trainable tokens.

Run `scripts/list_target_modules.py` on a base model or user-defined `torch.nn.Module` when `target_modules` are unknown or a PEFT config is not matching expected layers.

## Standard Training Flow

1. Load a compatible base model from Transformers, timm, Diffusers, or a user-defined `torch.nn.Module`.
2. Pick a PEFT config class and set the right `task_type` when the model task has a known wrapper.
3. Decide `target_modules`, `target_parameters`, and `modules_to_save`.
4. Wrap the base model with `get_peft_model`.
5. Verify `print_trainable_parameters()` and targeted module names.
6. Train with `Trainer`, Accelerate, or a custom PyTorch loop.
7. Save the adapter with `model.save_pretrained(output_dir)`.

```python
from peft import LoraConfig, TaskType, get_peft_model
from transformers import AutoModelForCausalLM

base_model = AutoModelForCausalLM.from_pretrained("model-id")
peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
)
model = get_peft_model(base_model, peft_config)
model.print_trainable_parameters()
```

## Decision Points

Use LoRA for the default low-rank adapter path. It is the broadest and best-documented method, works with many model families, and supports variants such as DoRA, rsLoRA, LoftQ, PiSSA, OLoRA, EVA, CorDA, LoRA-GA, trainable tokens, target parameters, and QLoRA-style all-linear targeting.

Use prompt tuning, p-tuning, prefix tuning, or multitask prompt tuning for soft-prompt approaches on language-model tasks where learning virtual tokens is preferable to modifying internal modules.

Use IA3 when the user wants very small learned vectors and the model architecture has clear attention and feed-forward targets.

Use `modules_to_save` when a task head, classifier, pooler, embedding, or other non-adapter layer must be trained and saved with the adapter.

Use `target_modules="all-linear"` for QLoRA-like LoRA across linear layers, especially with quantized LLM training.

Use `target_parameters` only when the target is an `nn.Parameter` rather than an `nn.Module`, such as some fused MoE weights. Some composition operations do not support parameter-targeted adapters.

## Verification

After wrapping:

```python
model.print_trainable_parameters()
print(getattr(model, "targeted_module_names", None))
```

For a suspicious trainable count, print or list modules:

```python
for name, module in model.named_modules():
    print(name, type(module))
```

For custom models, run `scripts/list_target_modules.py` or adapt its filtering logic.

## Common Mistakes

- Calling `get_peft_model` twice on the same model without unloading first.
- Loading a trained adapter for inference with `get_peft_model` instead of `PeftModel.from_pretrained`.
- Omitting `task_type` on task-specific Transformers models and then missing task-head handling.
- Forgetting `modules_to_save` for randomly initialized classification heads.
- Setting `target_modules` from another architecture without checking `named_modules()`.
- Using prompt-learning configs on arbitrary non-language modules.
- Adding tokens to a tokenizer but not resizing and saving/loading embeddings consistently.
