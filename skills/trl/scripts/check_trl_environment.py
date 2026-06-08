#!/usr/bin/env python3
"""Check that a public TRL environment can be inspected safely.

This script imports TRL, verifies stable trainer symbols, checks the CLI entry
point, and reports optional backend availability. It does not download models,
start servers, or run training.

Example:
    python skills/trl/scripts/check_trl_environment.py
"""

from __future__ import annotations

import importlib
import importlib.metadata as metadata
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    report: dict[str, object] = {
        "python": sys.version.split()[0],
        "executable": sys.executable,
        "ok": True,
        "errors": [],
        "optional": {},
    }

    try:
        import trl

        report["trl_version"] = metadata.version("trl")
        report["trl_module"] = getattr(trl, "__file__", None)
        stable = [
            "SFTTrainer",
            "SFTConfig",
            "DPOTrainer",
            "DPOConfig",
            "GRPOTrainer",
            "GRPOConfig",
            "RewardTrainer",
            "RewardConfig",
            "RLOOTrainer",
            "RLOOConfig",
        ]
        missing = [name for name in stable if not hasattr(trl, name)]
        report["stable_symbols_missing"] = missing
        if missing:
            report["ok"] = False
            report["errors"].append(f"Missing stable TRL symbols: {', '.join(missing)}")
    except Exception as exc:
        report["ok"] = False
        report["errors"].append(f"Could not import TRL: {type(exc).__name__}: {exc}")

    scripts_dir = Path(sys.executable).resolve().parent
    local_trl = scripts_dir / ("trl.exe" if sys.platform.startswith("win") else "trl")
    trl_exe = str(local_trl) if local_trl.exists() else None
    if trl_exe is None:
        import shutil

        trl_exe = shutil.which("trl")
    report["trl_cli"] = trl_exe
    if trl_exe:
        proc = subprocess.run([trl_exe, "--help"], text=True, capture_output=True, timeout=30, check=False)
        report["trl_cli_help_returncode"] = proc.returncode
        if proc.returncode != 0:
            report["ok"] = False
            report["errors"].append("`trl --help` failed")
    else:
        report["ok"] = False
        report["errors"].append("`trl` CLI entry point was not found on PATH")

    for package in ["torch", "peft", "vllm", "deepspeed", "liger_kernel", "bitsandbytes"]:
        try:
            module = importlib.import_module(package)
            report["optional"][package] = {
                "available": True,
                "version": getattr(module, "__version__", None),
            }
        except Exception as exc:
            report["optional"][package] = {
                "available": False,
                "error": f"{type(exc).__name__}: {exc}",
            }

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
