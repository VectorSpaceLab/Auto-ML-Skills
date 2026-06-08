#!/usr/bin/env python
"""List candidate PEFT target modules for a model.

Usage examples:
    python list_target_modules.py --model-id bert-base-uncased --task sequence-classification
    python list_target_modules.py --model-id gpt2 --task causal-lm --contains c_attn c_proj

The script may download a Transformers model if --model-id is a Hub id. It does
not train or modify the model.
"""

from __future__ import annotations

import argparse
import json


def load_model(model_id: str, task: str):
    from transformers import (
        AutoModel,
        AutoModelForCausalLM,
        AutoModelForQuestionAnswering,
        AutoModelForSeq2SeqLM,
        AutoModelForSequenceClassification,
        AutoModelForTokenClassification,
    )

    mapping = {
        "auto": AutoModel,
        "causal-lm": AutoModelForCausalLM,
        "seq2seq-lm": AutoModelForSeq2SeqLM,
        "sequence-classification": AutoModelForSequenceClassification,
        "token-classification": AutoModelForTokenClassification,
        "question-answering": AutoModelForQuestionAnswering,
    }
    return mapping[task].from_pretrained(model_id)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-id", required=True)
    parser.add_argument(
        "--task",
        choices=["auto", "causal-lm", "seq2seq-lm", "sequence-classification", "token-classification", "question-answering"],
        default="auto",
    )
    parser.add_argument(
        "--contains",
        nargs="*",
        default=["q_proj", "v_proj", "k_proj", "o_proj", "query", "value", "key", "c_attn", "c_proj", "linear", "fc", "dense", "classifier", "score", "lm_head"],
        help="Name fragments used to highlight candidate modules.",
    )
    args = parser.parse_args()

    model = load_model(args.model_id, args.task)
    rows = []
    for name, module in model.named_modules():
        if not name:
            continue
        module_type = type(module).__module__ + "." + type(module).__name__
        matched = [fragment for fragment in args.contains if fragment in name.lower()]
        if matched:
            rows.append({"name": name, "type": module_type, "matched": matched})

    print(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
