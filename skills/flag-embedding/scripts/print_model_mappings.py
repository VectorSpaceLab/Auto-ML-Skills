#!/usr/bin/env python3
"""Print FlagEmbedding auto model mappings from the installed package.

Example:
    python scripts/print_model_mappings.py
"""

from __future__ import annotations


def main() -> None:
    from FlagEmbedding.inference.embedder.model_mapping import AUTO_EMBEDDER_MAPPING
    from FlagEmbedding.inference.reranker.model_mapping import AUTO_RERANKER_MAPPING

    print("# Embedder mappings")
    for name, cfg in AUTO_EMBEDDER_MAPPING.items():
        print(
            f"{name}\tclass={cfg.model_class.__name__}"
            f"\tpooling={cfg.pooling_method.value}"
            f"\ttrust_remote_code={cfg.trust_remote_code}"
            f"\tquery_instruction_format={cfg.query_instruction_format!r}"
        )

    print("\n# Reranker mappings")
    for name, cfg in AUTO_RERANKER_MAPPING.items():
        print(
            f"{name}\tclass={cfg.model_class.__name__}"
            f"\ttrust_remote_code={cfg.trust_remote_code}"
        )


if __name__ == "__main__":
    main()
