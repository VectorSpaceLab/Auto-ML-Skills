#!/usr/bin/env python3
"""Initialize standalone PiSSA or LoftQ adapters with PEFT.

This is a self-contained adaptation of the public LLaMA-Factory utility scripts;
it does not require a source checkout.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def parse_targets(text: str) -> list[str]:
    return [item.strip() for item in text.split(",") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=["pissa", "loftq"], required=True)
    parser.add_argument("--model-name-or-path", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--lora-rank", type=int, default=16)
    parser.add_argument("--lora-alpha", type=int, default=None)
    parser.add_argument("--lora-dropout", type=float, default=0.0)
    parser.add_argument("--lora-target", default="q_proj,v_proj")
    parser.add_argument("--pissa-iter", type=int, default=16)
    parser.add_argument("--loftq-bits", type=int, default=4)
    parser.add_argument("--loftq-iter", type=int, default=4)
    parser.add_argument("--no-safetensors", action="store_true")
    args = parser.parse_args()

    from peft import LoftQConfig, LoraConfig, TaskType, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(args.model_name_or_path, trust_remote_code=True, torch_dtype="auto")
    kwargs = {}
    if args.kind == "pissa":
        kwargs["init_lora_weights"] = "pissa" if args.pissa_iter == -1 else f"pissa_niter_{args.pissa_iter}"
        adapter_name = "pissa_init"
    else:
        kwargs["init_lora_weights"] = "loftq"
        kwargs["loftq_config"] = LoftQConfig(loftq_bits=args.loftq_bits, loftq_iter=args.loftq_iter)
        kwargs["inference_mode"] = True
        adapter_name = "loftq_init"

    config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=args.lora_rank,
        lora_alpha=args.lora_alpha if args.lora_alpha is not None else args.lora_rank * 2,
        lora_dropout=args.lora_dropout,
        target_modules=parse_targets(args.lora_target),
        **kwargs,
    )
    peft_model = get_peft_model(model, config)
    adapter_dir = args.output_dir / adapter_name
    safe = not args.no_safetensors
    setattr(peft_model.peft_config["default"], "base_model_name_or_path", str(args.output_dir.resolve()))
    setattr(peft_model.peft_config["default"], "init_lora_weights", True)
    peft_model.save_pretrained(adapter_dir, safe_serialization=safe)
    base_model = peft_model.unload()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    base_model.save_pretrained(args.output_dir, safe_serialization=safe)
    tokenizer.save_pretrained(args.output_dir)
    print(f"model_name_or_path: {args.output_dir}")
    print(f"adapter_name_or_path: {adapter_dir}")
    print("finetuning_type: lora")
    if args.kind == "pissa":
        print("pissa_init: false")
        print("pissa_convert: true")
    else:
        print(f"quantization_bit: {args.loftq_bits}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
