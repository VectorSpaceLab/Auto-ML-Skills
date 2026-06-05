#!/usr/bin/env python3
"""Inspect public SGLang API and selected signatures without loading a model."""

import argparse
import importlib
import importlib.metadata as metadata
import inspect
import json


def signature(obj):
    try:
        return str(inspect.signature(obj))
    except Exception as exc:
        return f"<unavailable: {type(exc).__name__}>"


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect installed SGLang API signatures.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    parser.add_argument("--deep", action="store_true", help="Also inspect heavier server modules.")
    args = parser.parse_args()

    report = {"version": None, "symbols": {}, "modules": {}}
    try:
        report["version"] = metadata.version("sglang")
    except metadata.PackageNotFoundError:
        report["version"] = None

    try:
        import sglang as sgl

        for name in [
            "Runtime",
            "RuntimeEndpoint",
            "set_default_backend",
            "function",
            "system",
            "user",
            "assistant",
            "gen",
            "select",
            "image",
            "flush_cache",
        ]:
            obj = getattr(sgl, name, None)
            report["symbols"][name] = None if obj is None else signature(obj)
    except Exception as exc:
        report["symbols"]["sglang_import_error"] = f"{type(exc).__name__}: {exc}"

    modules = {
        "sglang.srt.sampling.sampling_params": ["SamplingParams"],
        "sglang.lang.backend.runtime_endpoint": ["RuntimeEndpoint"],
    }
    if args.deep:
        modules["sglang.srt.server_args"] = ["ServerArgs", "prepare_server_args"]
    for mod_name, names in modules.items():
        try:
            mod = importlib.import_module(mod_name)
            report["modules"][mod_name] = {name: signature(getattr(mod, name)) for name in names if hasattr(mod, name)}
        except Exception as exc:
            report["modules"][mod_name] = {"error": f"{type(exc).__name__}: {exc}"}

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
