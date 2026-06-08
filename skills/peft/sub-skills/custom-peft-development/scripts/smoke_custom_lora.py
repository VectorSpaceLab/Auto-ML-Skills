#!/usr/bin/env python
"""Smoke test PEFT LoRA on a small custom torch module.

Usage:
    python smoke_custom_lora.py

This is safe and self-contained: no downloads, credentials, or long training.
"""

from __future__ import annotations

import json
import tempfile

import torch
from torch import nn

from peft import LoraConfig, PeftModel, get_peft_model


class TinyMLP(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.lin0 = nn.Linear(4, 8)
        self.act = nn.ReLU()
        self.lin1 = nn.Linear(8, 2)

    def forward(self, x):
        return self.lin1(self.act(self.lin0(x)))


def main() -> int:
    torch.manual_seed(0)
    base = TinyMLP()
    config = LoraConfig(target_modules=["lin0"], modules_to_save=["lin1"], r=2, lora_alpha=4)
    model = get_peft_model(base, config)

    x = torch.randn(3, 4)
    y = model(x).sum()
    y.backward()

    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())

    with tempfile.TemporaryDirectory() as tmpdir:
        model.save_pretrained(tmpdir)
        fresh_base = TinyMLP()
        loaded = PeftModel.from_pretrained(fresh_base, tmpdir)
        out = loaded(x)

    report = {
        "status": "ok",
        "trainable_parameters": trainable,
        "total_parameters": total,
        "output_shape": list(out.shape),
        "targeted_module_names": getattr(model, "targeted_module_names", None),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
