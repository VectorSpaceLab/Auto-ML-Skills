#!/usr/bin/env python
"""Check a loaded PEFT/quantized model object for common deployment facts.

Copy this helper into a script where `model` is already loaded, then call:

    from check_quantized_peft import describe_model
    print(describe_model(model))

It does not load or modify models. The optional merge check only reports whether
the model exposes merge methods; it does not call them.
"""

from __future__ import annotations

import json


def describe_model(model) -> str:
    trainable = 0
    total = 0
    quantized_modules = []

    for name, param in model.named_parameters():
        total += param.numel()
        if param.requires_grad:
            trainable += param.numel()

    for name, module in model.named_modules():
        module_type = type(module).__module__ + "." + type(module).__name__
        lower = module_type.lower()
        if any(key in lower for key in ["bitsandbytes", "gptq", "aqlm", "hqq", "eetq", "torchao", "quant"]):
            quantized_modules.append({"name": name, "type": module_type})

    report = {
        "model_class": type(model).__module__ + "." + type(model).__name__,
        "trainable_parameters": trainable,
        "total_parameters": total,
        "trainable_percent": (100 * trainable / total) if total else None,
        "has_merge_and_unload": hasattr(model, "merge_and_unload"),
        "has_get_model_status": hasattr(model, "get_model_status"),
        "quantized_module_count": len(quantized_modules),
        "quantized_module_examples": quantized_modules[:20],
    }

    return json.dumps(report, indent=2, sort_keys=True)
