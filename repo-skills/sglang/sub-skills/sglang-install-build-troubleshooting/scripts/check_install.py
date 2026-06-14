#!/usr/bin/env python3
"""SGLang install troubleshooting probe."""

import argparse
import importlib
import importlib.metadata as metadata
import json
import os
import platform
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Check SGLang install, imports, device visibility, and key env vars.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = {
        "python": sys.version,
        "platform": platform.platform(),
        "packages": {},
        "imports": {},
        "env": {k: os.environ.get(k) for k in [
            "CUDA_HOME",
            "CUDA_VISIBLE_DEVICES",
            "ROCM_HOME",
            "SGLANG_CACHE_DIR",
            "SGLANG_USE_MODELSCOPE",
            "SGLANG_IS_FLASHINFER_AVAILABLE",
        ]},
        "torch": {},
    }
    for pkg in ["sglang", "sglang-kernel", "torch", "transformers", "xgrammar", "llguidance", "outlines"]:
        try:
            report["packages"][pkg] = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            report["packages"][pkg] = None
    for mod in ["sglang", "sglang.srt.server_args", "sglang.srt.sampling.sampling_params"]:
        try:
            importlib.import_module(mod)
            report["imports"][mod] = "ok"
        except Exception as exc:
            report["imports"][mod] = f"{type(exc).__name__}: {exc}"
    try:
        import torch
        report["torch"] = {
            "cuda_available": torch.cuda.is_available(),
            "device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
            "cuda_version": torch.version.cuda,
        }
    except Exception as exc:
        report["torch"] = {"error": f"{type(exc).__name__}: {exc}"}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
