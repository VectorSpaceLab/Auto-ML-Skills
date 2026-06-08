#!/usr/bin/env python3
"""
Self-contained SparseEncoder semantic search example.

Example:
  python sparse_semantic_search.py --query "What explores Mars?"
"""

from __future__ import annotations

import argparse

from sentence_transformers import SparseEncoder
from sentence_transformers.util import semantic_search


DEFAULT_CORPUS = [
    "Machine learning gives computers the ability to learn from data.",
    "Neural networks are computing systems inspired by biological networks.",
    "Mars rovers explore the surface of Mars and collect scientific data.",
    "The James Webb Space Telescope observes the universe in infrared light.",
    "Renewable energy sources include solar, wind, hydro, and geothermal power.",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="naver/splade-cocondenser-ensembledistil")
    parser.add_argument("--query", action="append", default=["What technology explores Mars?"])
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Validate arguments and print the planned workflow without loading a model.")
    args = parser.parse_args()

    if args.dry_run:
        print("DRY RUN: would load SparseEncoder:", args.model)
        print("DRY RUN: would encode corpus with encode_document and queries with encode_query")
        print("DRY RUN: would search with score_function=model.similarity and decode active tokens")
        print("DRY RUN: queries:", args.query)
        return 0

    model = SparseEncoder(args.model, local_files_only=args.local_files_only)
    corpus_embeddings = model.encode_document(DEFAULT_CORPUS, convert_to_tensor=True, convert_to_sparse_tensor=True)
    query_embeddings = model.encode_query(args.query, convert_to_tensor=True, convert_to_sparse_tensor=True)
    results = semantic_search(
        query_embeddings,
        corpus_embeddings,
        top_k=min(args.top_k, len(DEFAULT_CORPUS)),
        score_function=model.similarity,
    )

    stats = SparseEncoder.sparsity(corpus_embeddings)
    print(f"Corpus sparsity: {stats['sparsity_ratio']:.2%}; active dims: {stats['active_dims']:.2f}")
    for query_id, (query, hits) in enumerate(zip(args.query, results)):
        print(f"Query: {query}")
        pointwise = model.intersection(query_embeddings[query_id], corpus_embeddings)
        for hit in hits:
            tokens = model.decode(pointwise[hit["corpus_id"]], top_k=5)
            token_text = ", ".join(f"{token.strip()}={value:.2f}" for token, value in tokens)
            print(f"{hit['score']:.4f}\t{DEFAULT_CORPUS[hit['corpus_id']]}\t[{token_text}]")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
