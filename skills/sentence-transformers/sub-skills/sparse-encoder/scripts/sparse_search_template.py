#!/usr/bin/env python
"""Small in-memory sparse semantic-search template."""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run sparse semantic search over a tiny in-memory corpus.")
    parser.add_argument("--model", default="naver/splade-cocondenser-ensembledistil")
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--top-k", type=int, default=3)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    from sentence_transformers import SparseEncoder
    from sentence_transformers.util import semantic_search

    corpus = [
        "Neural networks are computing systems inspired by brains.",
        "Mars rovers collect data on the surface of Mars.",
        "Renewable energy includes solar and wind power.",
        "Vector databases can index sparse and dense vectors.",
    ]
    queries = ["How do artificial neural networks work?"]

    model = SparseEncoder(args.model, local_files_only=args.local_files_only)
    corpus_embeddings = model.encode_document(corpus, convert_to_sparse_tensor=True)
    query_embeddings = model.encode_query(queries, convert_to_sparse_tensor=True)
    hits = semantic_search(
        query_embeddings,
        corpus_embeddings,
        top_k=min(args.top_k, len(corpus)),
        score_function=model.similarity,
    )

    pointwise = model.intersection(query_embeddings[0], corpus_embeddings)
    for hit in hits[0]:
        terms = model.decode(pointwise[hit["corpus_id"]], top_k=5)
        print(f"{hit['score']:.4f}\t{corpus[hit['corpus_id']]}\tterms={terms}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
