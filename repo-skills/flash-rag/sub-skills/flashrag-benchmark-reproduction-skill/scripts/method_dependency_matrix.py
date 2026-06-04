#!/usr/bin/env python3
"""Print FlashRAG benchmark method dependency notes."""

from __future__ import annotations

import argparse


DEPS = {
    "naive": "Base generator, dataset, and optional retrieval docs only.",
    "zero-shot": "Base generator and dataset; no retrieval index required unless configured.",
    "AAR-contriever": "AAR retriever checkpoint plus a separately built AAR index.",
    "llmlingua": "Compressor/refiner model such as Llama2-7B; inspect compressed prompts.",
    "recomp": "Abstractive compressor checkpoint, preferably dataset-specific.",
    "selective-context": "GPT2 or configured selective-context refiner model.",
    "ret-robust": "Llama2-13B base model plus dataset-appropriate Ret-Robust LoRA.",
    "sure": "Base generator plus SuRe prompt/config choices.",
    "replug": "Base retriever/generator; document scores must be preserved.",
    "skr": "Encoder model plus inference-time training-data JSON.",
    "flare": "Base retriever/generator with active retrieval config.",
    "iterretgen": "Base retriever/generator with iterative loop settings.",
    "ircot": "Demonstration prompt and multi-hop settings.",
    "trace": "Triple extraction and evidence-chain prompt/model settings.",
    "selfrag": "Self-RAG generator checkpoint; use vLLM backend.",
    "spring": "Virtual token embedding file; use HF backend.",
    "adaptive": "Query classifier checkpoint; verify whether it is official or third-party.",
    "rqrag": "RQRAG generator checkpoint.",
    "r1searcher": "R1-Searcher generator checkpoint.",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Show FlashRAG method dependency notes.")
    parser.add_argument("method", nargs="?", help="Method name; omit to list all.")
    args = parser.parse_args()
    if args.method:
        key = next((k for k in DEPS if k.lower() == args.method.lower()), None)
        if key is None:
            raise SystemExit(f"Unknown method {args.method!r}. Known: {', '.join(sorted(DEPS))}")
        print(f"{key}: {DEPS[key]}")
    else:
        for key in sorted(DEPS):
            print(f"{key}: {DEPS[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
