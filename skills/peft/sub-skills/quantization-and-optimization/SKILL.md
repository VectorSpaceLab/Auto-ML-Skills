---
name: quantization-and-optimization
description: "Use this sub-skill for PEFT with quantized models, QLoRA, bitsandbytes, GPTQ, AQLM, EETQ, HQQ, torchao, INC, LoftQ, adapter dtype, low-memory loading, DoRA offload, and torch.compile."
---

# Quantization And Optimization

Use this sub-skill when the user mentions QLoRA, quantized LLM training, `BitsAndBytesConfig`, GPTQ, AQLM, EETQ, HQQ, torchao, Intel Neural Compressor, LoftQ, adapter dtype, low-memory loading, DoRA offload, or `torch.compile`.

Read `references/quantized-training.md` for QLoRA and quantizer-specific guidance.

Read `references/performance.md` for dtype, memory, DoRA, low CPU memory, and `torch.compile` guidance.

Run `scripts/check_quantized_peft.py` after loading a model when the user needs to verify quantization-related imports, CUDA visibility, PEFT wrapping, trainable parameters, and optional merge support.

## QLoRA Shape

```python
import torch
from peft import LoraConfig, TaskType, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

base_model = AutoModelForCausalLM.from_pretrained(
    "model-id",
    quantization_config=bnb_config,
    device_map="auto",
)
base_model = prepare_model_for_kbit_training(base_model)

peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    target_modules="all-linear",
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
)
model = get_peft_model(base_model, peft_config)
```

For LoftQ-friendly LoRA, use `target_modules="all-linear"` and NF4 4-bit quantization where the model and environment support bitsandbytes.

## Dtype And AMP

If training fails with FP16 gradient unscale errors, keep trainable adapter weights in fp32 or use:

```python
from peft import cast_mixed_precision_params

cast_mixed_precision_params(model, dtype=torch.float16)
```

Do not set `autocast_adapter_dtype=False` unless the user deliberately wants lower precision adapter weights and accepts stability risk.

## Merge Caution

Quantized merge support depends on the quantizer, adapter type, and dtype:

- Keep quantized base model and adapter separate unless merge support is documented and tested.
- AQLM adapters should remain separate.
- INC quantized paths do not support merge/unmerge in the documented guide.
- torchao merge is safest for LoRA with `int8_weight_only`; other combinations may fail or be incorrect.

## `torch.compile`

Load all adapters before compiling. Then compare compiled and uncompiled outputs on a small deterministic input. PEFT can work with compile, but dynamic adapter operations can cause graph breaks or wrong results.
