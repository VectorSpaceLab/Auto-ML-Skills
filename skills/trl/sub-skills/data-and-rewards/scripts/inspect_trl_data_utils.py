#!/usr/bin/env python3
"""Print public TRL data and reward utility signatures.

This script is read-only and safe. It helps future agents confirm the installed
TRL version's utility surface before writing dataset conversion or reward code.
"""

from __future__ import annotations

import importlib
import inspect
import json


def collect(module_name: str) -> list[dict[str, str]]:
    module = importlib.import_module(module_name)
    rows = []
    for name in dir(module):
        if name.startswith("_"):
            continue
        obj = getattr(module, name)
        if not (inspect.isfunction(obj) or inspect.isclass(obj)):
            continue
        obj_module = getattr(obj, "__module__", "")
        if not obj_module.startswith("trl"):
            continue
        try:
            target = obj if inspect.isfunction(obj) else obj.__init__
            signature = str(inspect.signature(target))
        except Exception as exc:
            signature = f"<unavailable: {type(exc).__name__}: {exc}>"
        rows.append({"name": name, "module": obj_module, "signature": signature})
    return rows


def main() -> int:
    print(json.dumps({"trl.data_utils": collect("trl.data_utils"), "trl.rewards": collect("trl.rewards")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
