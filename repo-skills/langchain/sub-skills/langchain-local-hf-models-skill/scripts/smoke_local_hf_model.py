#!/usr/bin/env python3
"""Smoke-test a local Hugging Face causal LM and optional LangChain wrapper."""

from __future__ import annotations

import argparse
import importlib.util
import json
import time
from pathlib import Path


def module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-path", required=True, help="Local model directory or model id.")
    parser.add_argument("--prompt", default="Say OK in one short sentence.")
    parser.add_argument("--max-new-tokens", type=int, default=16)
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--skip-langchain", action="store_true")
    args = parser.parse_args()

    result: dict[str, object] = {
        "model_path_is_dir": Path(args.model_path).expanduser().is_dir(),
        "imports": {
            "torch": module_available("torch"),
            "transformers": module_available("transformers"),
            "langchain_huggingface": module_available("langchain_huggingface"),
        },
        "raw_generation": None,
        "langchain_generation": None,
    }
    if not (result["imports"]["torch"] and result["imports"]["transformers"]):
        result["pass"] = False
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    start = time.time()
    tokenizer = AutoTokenizer.from_pretrained(args.model_path)
    use_cuda = args.device == "cuda" or (args.device == "auto" and torch.cuda.is_available())
    device = "cuda" if use_cuda else "cpu"
    model = AutoModelForCausalLM.from_pretrained(args.model_path)
    model.to(device)
    model.eval()

    if hasattr(tokenizer, "apply_chat_template"):
        try:
            prompt_text = tokenizer.apply_chat_template(
                [{"role": "user", "content": args.prompt}],
                tokenize=False,
                add_generation_prompt=True,
            )
        except TypeError:
            prompt_text = args.prompt
    else:
        prompt_text = args.prompt

    inputs = tokenizer(prompt_text, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=args.max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    generated_ids = outputs[0][inputs["input_ids"].shape[-1] :]
    generated_text = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
    result["raw_generation"] = {
        "device": device,
        "elapsed_seconds": round(time.time() - start, 3),
        "text_len": len(generated_text),
        "text": generated_text[:300],
    }

    if not args.skip_langchain and result["imports"]["langchain_huggingface"]:
        lc_start = time.time()
        from langchain_huggingface import HuggingFacePipeline

        llm = HuggingFacePipeline.from_model_id(
            model_id=args.model_path,
            task="text-generation",
            pipeline_kwargs={
                "max_new_tokens": args.max_new_tokens,
                "do_sample": False,
                "return_full_text": False,
            },
        )
        lc_text = llm.invoke(args.prompt)
        result["langchain_generation"] = {
            "elapsed_seconds": round(time.time() - lc_start, 3),
            "text_len": len(str(lc_text).strip()),
            "text": str(lc_text).strip()[:300],
        }

    result["pass"] = bool(generated_text)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
