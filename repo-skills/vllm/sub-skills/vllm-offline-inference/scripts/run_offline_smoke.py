#!/usr/bin/env python3
"""Dry-run or execute a small vLLM offline generation/chat smoke test."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from time import monotonic


def build_payload(args: argparse.Namespace) -> dict:
    return {
        "model": args.report_model_name or args.model,
        "mode": args.mode,
        "prompts": args.prompt,
        "sampling_params": {
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
        },
        "generation_config": args.generation_config,
        "engine_args": {
            "dtype": args.dtype,
            "max_model_len": args.max_model_len,
            "gpu_memory_utilization": args.gpu_memory_utilization,
            "enforce_eager": args.enforce_eager,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="Qwen/Qwen3-0.6B", help="Public model id or user-provided path.")
    parser.add_argument("--prompt", action="append", default=None, help="Prompt. Repeat for batch.")
    parser.add_argument("--mode", choices=["generate", "chat"], default="generate")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=16)
    parser.add_argument("--generation-config", default="vllm")
    parser.add_argument("--dtype", default="auto")
    parser.add_argument("--max-model-len", type=int, default=None)
    parser.add_argument("--gpu-memory-utilization", type=float, default=None)
    parser.add_argument("--enforce-eager", action="store_true")
    parser.add_argument("--report-model-name", default=None, help="Redacted/display model name for saved reports.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned payload without importing/loading vLLM.")
    parser.add_argument("--out", default=None, help="Optional JSON output path.")
    args = parser.parse_args()
    if args.prompt is None:
        args.prompt = ["Say hello in one short sentence."]
    result = {"request": build_payload(args), "dry_run": args.dry_run}
    started = monotonic()
    if not args.dry_run:
        try:
            from vllm import LLM, SamplingParams

            llm_kwargs = {
                "model": args.model,
                "generation_config": args.generation_config,
                "dtype": args.dtype,
            }
            if args.max_model_len is not None:
                llm_kwargs["max_model_len"] = args.max_model_len
            if args.gpu_memory_utilization is not None:
                llm_kwargs["gpu_memory_utilization"] = args.gpu_memory_utilization
            if args.enforce_eager:
                llm_kwargs["enforce_eager"] = True
            llm = LLM(**llm_kwargs)
            params = SamplingParams(temperature=args.temperature, max_tokens=args.max_tokens)
            if args.mode == "chat":
                messages = [[{"role": "user", "content": prompt}] for prompt in args.prompt]
                outputs = llm.chat(messages, params)
            else:
                outputs = llm.generate(args.prompt, params)
            result["ok"] = True
            result["outputs"] = [
                {
                    "prompt": getattr(output, "prompt", None),
                    "text": output.outputs[0].text if output.outputs else "",
                    "token_count": len(output.outputs[0].token_ids) if output.outputs else 0,
                }
                for output in outputs
            ]
        except Exception as exc:  # pragma: no cover - diagnostic script path
            result["ok"] = False
            result["error_type"] = type(exc).__name__
            result["error"] = str(exc)
    result["elapsed_s"] = round(monotonic() - started, 3)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
