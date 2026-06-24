#!/usr/bin/env python3
"""Load a local Transformers LM and call it from a LangGraph StateGraph node."""

from __future__ import annotations

import argparse
import json
import time

from typing_extensions import TypedDict


class State(TypedDict):
    prompt: str
    answer: str


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--prompt", default="Say OK in one short sentence.")
    parser.add_argument("--max-new-tokens", type=int, default=16)
    parser.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    args = parser.parse_args()

    import torch
    from langgraph.graph import END, START, StateGraph
    from transformers import AutoModelForCausalLM, AutoTokenizer

    start = time.time()
    tokenizer = AutoTokenizer.from_pretrained(args.model_path)
    use_cuda = args.device == "cuda" or (args.device == "auto" and torch.cuda.is_available())
    device = "cuda" if use_cuda else "cpu"
    model = AutoModelForCausalLM.from_pretrained(args.model_path)
    model.to(device)
    model.eval()

    def render_prompt(prompt: str) -> str:
        if hasattr(tokenizer, "apply_chat_template"):
            try:
                return tokenizer.apply_chat_template(
                    [{"role": "user", "content": prompt}],
                    tokenize=False,
                    add_generation_prompt=True,
                )
            except TypeError:
                return prompt
        return prompt

    def generate(state: State) -> dict[str, str]:
        prompt_text = render_prompt(state["prompt"])
        inputs = tokenizer(prompt_text, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=args.max_new_tokens,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
        generated_ids = outputs[0][inputs["input_ids"].shape[-1] :]
        answer = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
        return {"answer": answer}

    builder = StateGraph(State)
    builder.add_node("generate", generate)
    builder.add_edge(START, "generate")
    builder.add_edge("generate", END)
    graph = builder.compile()
    output = graph.invoke({"prompt": args.prompt, "answer": ""})

    result = {
        "device": device,
        "elapsed_seconds": round(time.time() - start, 3),
        "answer_len": len(output["answer"]),
        "answer": output["answer"][:300],
    }
    result["pass"] = bool(output["answer"])
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
