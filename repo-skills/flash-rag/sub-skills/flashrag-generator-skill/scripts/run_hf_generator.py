#!/usr/bin/env python3
"""Run a small local Hugging Face generator smoke test.

Purpose:
  Use this after `make_generator_config.py` and `render_prompt.py` when a
  future agent needs to prove that a local generator model path can actually
  load and generate, not just render a fake/offline response.

Example:
  python scripts/run_hf_generator.py \
    --config /tmp/generator.yaml \
    --prompt /tmp/prompt.txt \
    --output /tmp/generation.json \
    --device cuda:0 \
    --max-new-tokens 16
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import read_simple_yaml


def resolve_model_path(config: dict, override: str | None) -> str:
    model_path = override or config.get("generator_model_path") or config.get("generator_model")
    if not model_path:
        raise ValueError("provide --model-path or set generator_model_path in the config")
    return str(model_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a minimal HF local generator smoke test.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model-path", default=None, help="Override generator_model_path from the config.")
    parser.add_argument("--device", default="auto", help="Use 'auto', 'cpu', 'cuda', or a device like cuda:0.")
    parser.add_argument("--dtype", choices=["auto", "float32", "float16", "bfloat16"], default="auto")
    parser.add_argument("--max-new-tokens", type=int, default=None)
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--local-files-only", action="store_true")
    args = parser.parse_args()

    config = read_simple_yaml(args.config)
    model_path = resolve_model_path(config, args.model_path)
    prompt = args.prompt.read_text(encoding="utf-8")
    generation_params = config.get("generation_params") if isinstance(config.get("generation_params"), dict) else {}
    max_new_tokens = args.max_new_tokens or int(config.get("max_new_tokens") or generation_params.get("max_tokens") or 16)

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    dtype_map = {
        "auto": "auto",
        "float32": torch.float32,
        "float16": torch.float16,
        "bfloat16": torch.bfloat16,
    }
    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        trust_remote_code=args.trust_remote_code,
        local_files_only=args.local_files_only,
    )
    load_kwargs = {
        "trust_remote_code": args.trust_remote_code,
        "local_files_only": args.local_files_only,
        "torch_dtype": dtype_map[args.dtype],
    }
    if args.device == "auto":
        load_kwargs["device_map"] = "auto"
    model = AutoModelForCausalLM.from_pretrained(model_path, **load_kwargs)
    if args.device != "auto":
        model = model.to(args.device)

    inputs = tokenizer(prompt, return_tensors="pt")
    if args.device == "auto":
        target_device = next(model.parameters()).device
    else:
        target_device = torch.device(args.device)
    inputs = {key: value.to(target_device) for key, value in inputs.items()}

    model.eval()
    with torch.inference_mode():
        output_ids = model.generate(
            **inputs,
            do_sample=False,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id,
        )
    prompt_len = inputs["input_ids"].shape[-1]
    pred = tokenizer.decode(output_ids[0][prompt_len:], skip_special_tokens=True).strip()

    payload = {
        "model_path": model_path,
        "prompt": prompt,
        "prompt_chars": len(prompt),
        "max_new_tokens": max_new_tokens,
        "pred": pred,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pred": pred[:200], "output": str(args.output)}, ensure_ascii=False, indent=2))
    return 0 if pred else 1


if __name__ == "__main__":
    raise SystemExit(main())
