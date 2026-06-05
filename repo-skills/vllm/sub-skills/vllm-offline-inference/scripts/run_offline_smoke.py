#!/usr/bin/env python3
"""Dry-run or execute a small vLLM offline generation/chat smoke test."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_payload(args: argparse.Namespace) -> dict:
    return {
        "model": args.model,
        "mode": args.mode,
        "prompts": args.prompt,
        "sampling_params": {
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
        },
        "generation_config": args.generation_config,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="Qwen/Qwen3-0.6B", help="Public model id or user-provided path.")
    parser.add_argument("--prompt", action="append", default=["Say hello in one short sentence."], help="Prompt. Repeat for batch.")
    parser.add_argument("--mode", choices=["generate", "chat"], default="generate")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=16)
    parser.add_argument("--generation-config", default="vllm")
    parser.add_argument("--dry-run", action="store_true", help="Print planned payload without importing/loading vLLM.")
    parser.add_argument("--out", default=None, help="Optional JSON output path.")
    args = parser.parse_args()
    result = {"request": build_payload(args), "dry_run": args.dry_run}
    if not args.dry_run:
        from vllm import LLM, SamplingParams

        llm = LLM(model=args.model, generation_config=args.generation_config)
        params = SamplingParams(temperature=args.temperature, max_tokens=args.max_tokens)
        if args.mode == "chat":
            messages = [[{"role": "user", "content": prompt}] for prompt in args.prompt]
            outputs = llm.chat(messages, params)
        else:
            outputs = llm.generate(args.prompt, params)
        result["outputs"] = [
            {
                "prompt": getattr(output, "prompt", None),
                "text": output.outputs[0].text if output.outputs else "",
                "token_count": len(output.outputs[0].token_ids) if output.outputs else 0,
            }
            for output in outputs
        ]
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
