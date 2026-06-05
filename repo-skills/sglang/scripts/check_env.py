#!/usr/bin/env python3
"""Lightweight SGLang environment probe."""

import argparse
import importlib
import importlib.metadata as metadata
import json
import platform
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether SGLang can be imported and summarize runtime capabilities.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    parser.add_argument("--import-sglang", action="store_true", help="Import sglang and selected modules.")
    parser.add_argument("--deep", action="store_true", help="Also import heavier server modules; implies --import-sglang.")
    parser.add_argument("--torch", action="store_true", help="Import torch and check CUDA visibility.")
    args = parser.parse_args()

    out = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": {},
        "imports": {},
        "torch": {},
    }
    for pkg in ["sglang", "torch", "transformers", "openai", "fastapi", "uvicorn"]:
        try:
            out["packages"][pkg] = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            out["packages"][pkg] = None

    if args.import_sglang or args.deep:
        modules = ["sglang"]
        if args.deep:
            modules += ["sglang.srt.server_args", "sglang.srt.entrypoints.http_server"]
        for mod in modules:
            try:
                importlib.import_module(mod)
                out["imports"][mod] = "ok"
            except Exception as exc:
                out["imports"][mod] = f"{type(exc).__name__}: {exc}"

    if args.torch:
        try:
            import torch

            out["torch"] = {
                "cuda_available": bool(torch.cuda.is_available()),
                "cuda_device_count": int(torch.cuda.device_count()) if torch.cuda.is_available() else 0,
                "cuda_version": torch.version.cuda,
            }
        except Exception as exc:
            out["torch"] = {"error": f"{type(exc).__name__}: {exc}"}

    if args.json:
        print(json.dumps(out, indent=2, sort_keys=True))
    else:
        for section, value in out.items():
            print(f"{section}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
