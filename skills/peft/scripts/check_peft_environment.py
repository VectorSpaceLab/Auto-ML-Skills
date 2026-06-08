#!/usr/bin/env python
"""Check whether a Python environment can import and inspect core PEFT APIs.

Usage:
    python check_peft_environment.py
    python check_peft_environment.py --require-cuda

The script is read-only. It prints JSON so agents can paste the output into a
debugging report.
"""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata as metadata
import inspect
import json
import subprocess
import sys


def package_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-cuda", action="store_true", help="Fail if torch CUDA is unavailable.")
    args = parser.parse_args()

    report: dict[str, object] = {
        "python": sys.version.replace("\n", " "),
        "executable": sys.executable,
        "packages": {name: package_version(name) for name in ["peft", "torch", "transformers", "accelerate"]},
        "imports": {},
        "signatures": {},
        "pip_check": None,
        "torch": {},
        "status": "ok",
        "failures": [],
    }

    for module_name in ["peft", "torch", "transformers", "accelerate"]:
        try:
            module = importlib.import_module(module_name)
            report["imports"][module_name] = {"ok": True, "file": getattr(module, "__file__", None)}
        except Exception as exc:
            report["imports"][module_name] = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
            report["failures"].append(f"could not import {module_name}")

    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pip", "check"],
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        report["pip_check"] = {
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
        if proc.returncode != 0:
            report["failures"].append("pip check failed")
    except Exception as exc:
        report["pip_check"] = {"error": f"{type(exc).__name__}: {exc}"}
        report["failures"].append("pip check could not run")

    try:
        import torch

        torch_report = {
            "version": getattr(torch, "__version__", None),
            "cuda_version": getattr(torch.version, "cuda", None),
            "cuda_available": bool(torch.cuda.is_available()),
            "cuda_device_count": int(torch.cuda.device_count()),
        }
        if torch.cuda.is_available():
            torch_report["cuda_device_0"] = torch.cuda.get_device_name(0)
            torch_report["cuda_capability_0"] = list(torch.cuda.get_device_capability(0))
        report["torch"] = torch_report
        if args.require_cuda and not torch_report["cuda_available"]:
            report["failures"].append("CUDA was required but torch.cuda is unavailable")
    except Exception as exc:
        report["torch"] = {"error": f"{type(exc).__name__}: {exc}"}
        if args.require_cuda:
            report["failures"].append("CUDA was required but torch import/check failed")

    try:
        from peft import LoraConfig, PeftConfig, PeftModel, TaskType, get_peft_model

        report["signatures"] = {
            "get_peft_model": str(inspect.signature(get_peft_model)),
            "PeftModel.from_pretrained": str(inspect.signature(PeftModel.from_pretrained)),
            "PeftModel.save_pretrained": str(inspect.signature(PeftModel.save_pretrained)),
            "PeftConfig.from_pretrained": str(inspect.signature(PeftConfig.from_pretrained)),
            "LoraConfig": str(inspect.signature(LoraConfig)),
        }
        report["task_types"] = [f"{item.name}={item.value}" for item in TaskType]
    except Exception as exc:
        report["failures"].append(f"could not inspect PEFT public APIs: {type(exc).__name__}: {exc}")

    if report["failures"]:
        report["status"] = "failed"

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
