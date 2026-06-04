#!/usr/bin/env python
"""Small dense semantic-search template with no external dataset dependency.

This script downloads the selected model unless it is already cached or
--local-files-only is provided. It keeps the corpus tiny and is intended as a
copy/adapt starting point, not as a benchmark.
"""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run dense semantic search over a tiny in-memory corpus.")
    parser.add_argument("--model", default="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--top-k", type=int, default=3)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    from sentence_transformers import SentenceTransformer
    from sentence_transformers.util import dot_score, semantic_search

    corpus = [
        "Python is a programming language used for data science and web services.",
        "Mars is known as the Red Planet because of iron oxide on its surface.",
        "Vector databases index embeddings for efficient nearest-neighbor search.",
        "A Cross Encoder reranks candidate documents by scoring query-document pairs.",
    ]
    queries = ["What stores embeddings for search?", "Why is Mars red?"]

    model = SentenceTransformer(args.model, local_files_only=args.local_files_only)
    corpus_embeddings = model.encode_document(corpus, normalize_embeddings=True, convert_to_tensor=True)
    query_embeddings = model.encode_query(queries, normalize_embeddings=True, convert_to_tensor=True)
    hits = semantic_search(
        query_embeddings,
        corpus_embeddings,
        top_k=min(args.top_k, len(corpus)),
        score_function=dot_score,
    )

    for query, query_hits in zip(queries, hits):
        print(f"Query: {query}")
        for hit in query_hits:
            print(f"  {hit['score']:.4f}  {corpus[hit['corpus_id']]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
