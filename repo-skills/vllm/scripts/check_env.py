#!/usr/bin/env python3
"""Safe vLLM environment inspection without loading a model."""

from __future__ import annotations

import argparse
import os
import platform
import sys

from vllm_skill_common import (
    command_exists,
    console_scripts,
    import_status,
    package_version,
    print_json,
    run_short_command,
)


def build_report(args: argparse.Namespace) -> dict:
    report = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "executable_basename": os.path.basename(sys.executable),
        "vllm_version": package_version("vllm"),
        "torch_version": package_version("torch"),
        "transformers_version": package_version("transformers"),
        "console_scripts": console_scripts("vllm"),
        "imports": [],
        "commands": {},
        "env": {
            key: os.environ.get(key)
            for key in [
                "CUDA_VISIBLE_DEVICES",
                "HIP_VISIBLE_DEVICES",
                "VLLM_USE_MODELSCOPE",
                "VLLM_API_KEY",
                "VLLM_ALLOW_RUNTIME_LORA_UPDATING",
                "HF_HOME",
            ]
            if os.environ.get(key) is not None
        },
    }
    modules = ["vllm", "vllm.entrypoints.cli.main"]
    if args.deep_import:
        modules += [
            "vllm.entrypoints.llm",
            "vllm.sampling_params",
            "vllm.engine.arg_utils",
        ]
    report["imports"] = [import_status(module) for module in modules]
    if command_exists("vllm"):
        report["commands"]["vllm_help"] = run_short_command(
            ["vllm", "--help"], timeout=args.command_timeout
        )
    if command_exists("nvidia-smi"):
        report["commands"]["nvidia_smi"] = run_short_command(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
            timeout=args.command_timeout,
        )
    if command_exists("rocm-smi"):
        report["commands"]["rocm_smi"] = run_short_command(
            ["rocm-smi", "--showproductname"], timeout=args.command_timeout
        )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument(
        "--deep-import",
        action="store_true",
        help="Import additional vLLM modules. This is still model-free but may be slower.",
    )
    parser.add_argument(
        "--command-timeout",
        type=float,
        default=10.0,
        help="Timeout for optional CLI/platform commands.",
    )
    args = parser.parse_args()
    report = build_report(args)
    if args.json:
        print_json(report)
    else:
        print(f"python: {report['python']}")
        print(f"vllm: {report['vllm_version']}")
        print(f"torch: {report['torch_version']}")
        print(f"console_scripts: {report['console_scripts']}")
        for item in report["imports"]:
            print(f"import {item['module']}: {'ok' if item['ok'] else item.get('error')}")


if __name__ == "__main__":
    main()
