#!/usr/bin/env python3
"""Inspect vLLM public API names and signatures without loading a model."""

from __future__ import annotations

import argparse
import importlib
import inspect

from vllm_skill_common import console_scripts, package_version, print_json


DEFAULT_OBJECTS = [
    "vllm:LLM",
    "vllm:SamplingParams",
    "vllm:PoolingParams",
    "vllm.engine.arg_utils:EngineArgs",
    "vllm.engine.arg_utils:AsyncEngineArgs",
    "vllm.lora.request:LoRARequest",
    "vllm.entrypoints.openai.protocol:ChatCompletionRequest",
    "vllm.entrypoints.openai.protocol:CompletionRequest",
    "vllm.entrypoints.openai.protocol:EmbeddingRequest",
    "vllm.entrypoints.openai.protocol:ResponsesRequest",
    "vllm.entrypoints.openai.protocol:ScoreRequest",
]


def inspect_object(spec: str) -> dict:
    module_name, _, attr = spec.partition(":")
    result = {"spec": spec, "present": False}
    try:
        module = importlib.import_module(module_name)
        obj = getattr(module, attr)
        result["present"] = True
        result["type"] = type(obj).__name__
        try:
            result["signature"] = str(inspect.signature(obj))
        except Exception as exc:
            result["signature_error"] = f"{type(exc).__name__}: {exc}"
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print JSON.")
    parser.add_argument(
        "--object",
        action="append",
        default=[],
        help="Extra object spec as module:attribute.",
    )
    args = parser.parse_args()
    objects = DEFAULT_OBJECTS + args.object
    report = {
        "vllm_version": package_version("vllm"),
        "console_scripts": console_scripts("vllm"),
        "objects": [inspect_object(spec) for spec in objects],
    }
    if args.json:
        print_json(report)
    else:
        print(f"vllm: {report['vllm_version']}")
        print(f"console_scripts: {report['console_scripts']}")
        for obj in report["objects"]:
            line = f"{obj['spec']}: {'present' if obj['present'] else 'missing'}"
            if obj.get("signature"):
                line += f" {obj['signature']}"
            elif obj.get("error"):
                line += f" {obj['error']}"
            print(line)


if __name__ == "__main__":
    main()
