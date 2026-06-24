#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import emit


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a LLaMA-Factory chat/inference config.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--adapter", default=None)
    parser.add_argument("--template", default="qwen3_nothink")
    parser.add_argument("--backend", choices=["huggingface", "vllm", "sglang"], default="huggingface")
    parser.add_argument("--infer-dtype", choices=["auto", "float16", "bfloat16", "float32"], default="float32")
    parser.add_argument("--stage", choices=["sft", "rm"], default="sft")
    parser.add_argument("--finetuning-type", choices=["lora", "full"], default=None)
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--cutoff-len", type=int, default=2048)
    parser.add_argument("--max-new-tokens", type=int, default=64)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--top-p", type=float, default=0.7)
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--do-sample", choices=["true", "false"], default="false")
    args = parser.parse_args()

    finetuning_type = args.finetuning_type
    if finetuning_type is None:
        finetuning_type = "lora" if args.adapter else "full"
    cfg = {
        "model_name_or_path": args.model,
        "template": args.template,
        "infer_backend": args.backend,
        "trust_remote_code": args.trust_remote_code,
        "infer_dtype": args.infer_dtype,
        "stage": args.stage,
        "finetuning_type": finetuning_type,
        "cutoff_len": args.cutoff_len,
        "max_new_tokens": args.max_new_tokens,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "top_k": args.top_k,
        "do_sample": args.do_sample == "true",
    }
    if args.adapter:
        cfg["adapter_name_or_path"] = args.adapter
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(emit(cfg)) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
