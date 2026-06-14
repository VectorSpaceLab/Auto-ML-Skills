#!/usr/bin/env python3
"""Check a FlagEmbedding environment without downloading models.

Example:
    python scripts/check_flagembedding_env.py --show-torch
"""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata as metadata
import inspect
import json
import sys
from typing import Any


PUBLIC_OBJECTS = [
    "FlagAutoModel",
    "FlagModel",
    "BGEM3FlagModel",
    "FlagLLMModel",
    "FlagICLModel",
    "FlagAutoReranker",
    "FlagReranker",
    "FlagLLMReranker",
    "LayerWiseFlagLLMReranker",
    "LightWeightFlagLLMReranker",
]


def safe_signature(obj: Any) -> str:
    try:
        return str(inspect.signature(obj))
    except Exception as exc:  # pragma: no cover - diagnostic helper
        return f"<unavailable: {type(exc).__name__}: {exc}>"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--show-signatures", action="store_true", help="Print signatures for key public APIs.")
    parser.add_argument("--show-torch", action="store_true", help="Print torch version and backend availability.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = parser.parse_args()

    report: dict[str, Any] = {"ok": True, "python": sys.version.split()[0]}

    try:
        pkg = importlib.import_module("FlagEmbedding")
        report["distribution_version"] = metadata.version("FlagEmbedding")
        report["module_file"] = getattr(pkg, "__file__", None)
    except Exception as exc:
        report["ok"] = False
        report["error"] = f"{type(exc).__name__}: {exc}"
        print(json.dumps(report, indent=2) if args.json else report["error"])
        return 1

    objects: dict[str, Any] = {}
    for name in PUBLIC_OBJECTS:
        obj = getattr(pkg, name, None)
        objects[name] = {
            "present": obj is not None,
            "module": getattr(obj, "__module__", None) if obj is not None else None,
        }
        if args.show_signatures and obj is not None:
            objects[name]["signature"] = safe_signature(obj)
    report["public_objects"] = objects

    if args.show_torch:
        try:
            import torch

            torch_info: dict[str, Any] = {
                "version": torch.__version__,
                "cuda_version": getattr(torch.version, "cuda", None),
                "cuda_available": torch.cuda.is_available(),
                "cuda_device_count": torch.cuda.device_count(),
            }
            if torch.cuda.is_available():
                torch_info["cuda_device_0"] = torch.cuda.get_device_name(0)
                torch_info["cuda_capability_0"] = torch.cuda.get_device_capability(0)
            report["torch"] = torch_info
        except Exception as exc:
            report["torch"] = {"error": f"{type(exc).__name__}: {exc}"}

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"FlagEmbedding {report['distribution_version']} import: ok")
        print(f"module: {report['module_file']}")
        for name, info in objects.items():
            marker = "ok" if info["present"] else "missing"
            print(f"{name}: {marker}")
            if args.show_signatures and "signature" in info:
                print(f"  {info['signature']}")
        if "torch" in report:
            print("torch:", json.dumps(report["torch"], sort_keys=True))

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
