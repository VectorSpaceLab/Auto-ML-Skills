#!/usr/bin/env python3
"""Check a FlagEmbedding installation without downloading models.

Example:
    python check_install.py --json
"""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata as metadata
import json
import sys
from typing import Any


MODULES = [
    "FlagEmbedding",
    "FlagEmbedding.inference.auto_embedder",
    "FlagEmbedding.inference.auto_reranker",
    "FlagEmbedding.abc.inference.AbsEmbedder",
    "FlagEmbedding.abc.inference.AbsReranker",
]
OPTIONAL_FINE_TUNE = ["deepspeed", "flash_attn"]


def check_module(name: str) -> dict[str, Any]:
    try:
        module = importlib.import_module(name)
        return {"name": name, "ok": True, "file": bool(getattr(module, "__file__", None))}
    except Exception as exc:  # noqa: BLE001 - diagnostic script should report import failures clearly.
        return {"name": name, "ok": False, "error": f"{type(exc).__name__}: {exc}"}


def torch_status() -> dict[str, Any]:
    try:
        import torch
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    status: dict[str, Any] = {
        "ok": True,
        "version": getattr(torch, "__version__", None),
        "cuda_available": bool(torch.cuda.is_available()),
        "cuda_device_count": int(torch.cuda.device_count()) if torch.cuda.is_available() else 0,
    }
    try:
        status["mps_available"] = bool(torch.backends.mps.is_available())
    except Exception:
        status["mps_available"] = False
    return status


def main() -> int:
    parser = argparse.ArgumentParser(description="Check FlagEmbedding imports, metadata, Torch backend, and optional fine-tune dependencies.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--check-finetune-extra", action="store_true", help="Also report whether optional training accelerator modules import.")
    args = parser.parse_args()

    result: dict[str, Any] = {
        "python": sys.version.split()[0],
        "distribution": None,
        "imports": [check_module(name) for name in MODULES],
        "torch": torch_status(),
        "optional_finetune": [],
    }

    try:
        result["distribution"] = {"name": "FlagEmbedding", "version": metadata.version("FlagEmbedding")}
    except metadata.PackageNotFoundError:
        result["distribution"] = {"name": "FlagEmbedding", "error": "distribution metadata not found"}

    if args.check_finetune_extra:
        result["optional_finetune"] = [check_module(name) for name in OPTIONAL_FINE_TUNE]

    ok = all(item["ok"] for item in result["imports"]) and result["torch"].get("ok", False)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Python: {result['python']}")
        print(f"Distribution: {result['distribution']}")
        print(f"Torch: {result['torch']}")
        for item in result["imports"]:
            print(f"Import {item['name']}: {'OK' if item['ok'] else item['error']}")
        for item in result["optional_finetune"]:
            print(f"Optional {item['name']}: {'OK' if item['ok'] else item['error']}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
