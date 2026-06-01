#!/usr/bin/env python3
"""No-download inference smoke check for FlagEmbedding.

This validates imports, signatures, and auto mappings without constructing any
model instance. It is safe to run before network/model-cache access is allowed.

Example:
    python sub-skills/inference/scripts/smoke_inference_no_download.py
"""

from __future__ import annotations

import inspect


def main() -> None:
    from FlagEmbedding import (
        BGEM3FlagModel,
        FlagAutoModel,
        FlagAutoReranker,
        FlagICLModel,
        FlagLLMModel,
        FlagModel,
        FlagReranker,
    )
    from FlagEmbedding.inference.embedder.model_mapping import AUTO_EMBEDDER_MAPPING
    from FlagEmbedding.inference.reranker.model_mapping import AUTO_RERANKER_MAPPING

    objects = [
        FlagAutoModel.from_finetuned,
        FlagModel,
        BGEM3FlagModel,
        FlagLLMModel,
        FlagICLModel,
        FlagAutoReranker.from_finetuned,
        FlagReranker,
    ]
    for obj in objects:
        print(f"{obj}: {inspect.signature(obj)}")

    required_embedders = ["bge-m3", "bge-base-en-v1.5", "bge-en-icl", "bge-multilingual-gemma2"]
    required_rerankers = ["bge-reranker-v2-m3", "bge-reranker-v2-gemma", "bge-reranker-v2-minicpm-layerwise"]
    for name in required_embedders:
        print(f"embedder mapping {name}: {name in AUTO_EMBEDDER_MAPPING}")
    for name in required_rerankers:
        print(f"reranker mapping {name}: {name in AUTO_RERANKER_MAPPING}")


if __name__ == "__main__":
    main()
