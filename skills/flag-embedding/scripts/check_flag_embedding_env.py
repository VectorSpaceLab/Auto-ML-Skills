#!/usr/bin/env python3
"""Check a FlagEmbedding installation without downloading models.

Example:
    python scripts/check_flag_embedding_env.py
"""

from __future__ import annotations

import importlib.metadata as metadata
import inspect


def main() -> None:
    import FlagEmbedding
    from FlagEmbedding.inference.embedder.model_mapping import AUTO_EMBEDDER_MAPPING
    from FlagEmbedding.inference.reranker.model_mapping import AUTO_RERANKER_MAPPING

    print("FlagEmbedding module:", FlagEmbedding.__name__)
    try:
        dist = metadata.distribution("FlagEmbedding")
        print("Distribution:", dist.metadata["Name"], dist.version)
    except metadata.PackageNotFoundError:
        print("Distribution metadata not found; module import still succeeded.")

    exports = [
        "FlagAutoModel",
        "FlagModel",
        "BGEM3FlagModel",
        "FlagLLMModel",
        "FlagICLModel",
        "FlagPseudoMoEModel",
        "FlagAutoReranker",
        "FlagReranker",
        "FlagLLMReranker",
        "LayerWiseFlagLLMReranker",
        "LightWeightFlagLLMReranker",
    ]
    for name in exports:
        obj = getattr(FlagEmbedding, name, None)
        print(f"{name}: {'OK' if obj is not None else 'MISSING'}")
        if obj is not None:
            try:
                print(f"  signature: {inspect.signature(obj)}")
            except (TypeError, ValueError):
                pass
            if hasattr(obj, "from_finetuned"):
                print(f"  from_finetuned: {inspect.signature(obj.from_finetuned)}")

    print("Auto embedders:", len(AUTO_EMBEDDER_MAPPING))
    print("First embedder mappings:", ", ".join(list(AUTO_EMBEDDER_MAPPING)[:10]))
    print("Auto rerankers:", len(AUTO_RERANKER_MAPPING))
    print("Reranker mappings:", ", ".join(AUTO_RERANKER_MAPPING))


if __name__ == "__main__":
    main()
