#!/usr/bin/env python3
"""Inspect stable TRL trainer imports and constructor signatures.

This safe smoke test does not load model weights, download datasets, or start
training. It is useful before writing code that depends on stable TRL trainers.
"""

from __future__ import annotations

import inspect
import json


def main() -> int:
    import trl

    names = [
        "SFTConfig",
        "SFTTrainer",
        "DPOConfig",
        "DPOTrainer",
        "GRPOConfig",
        "GRPOTrainer",
        "RewardConfig",
        "RewardTrainer",
        "RLOOConfig",
        "RLOOTrainer",
    ]
    report = []
    for name in names:
        obj = getattr(trl, name)
        target = obj.__init__ if inspect.isclass(obj) else obj
        report.append(
            {
                "name": name,
                "module": getattr(obj, "__module__", None),
                "signature": str(inspect.signature(target)),
            }
        )
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
