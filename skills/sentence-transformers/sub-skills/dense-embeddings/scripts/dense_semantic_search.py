#!/usr/bin/env python3
"""
Self-contained dense semantic search example.

By default this uses a small in-memory corpus. It downloads the requested model
unless it is already cached or --local-files-only is set.

Example:
  python dense_semantic_search.py --query "How do neural networks work?"
"""

from __future__ import annotations

import argparse

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search


DEFAULT_CORPUS = [
    "Machine learning gives computers the ability to learn from data.",
    "Neural networks are computing systems inspired by biological networks.",
    "Mars rovers explore the surface of Mars and collect scientific data.",
    "The James Webb Space Telescope observes the universe in infrared light.",
    "Renewable energy sources include solar, wind, hydro, and geothermal power.",
    "Carbon capture technologies collect emissions before they enter the atmosphere.",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--query", action="append", default=["How do artificial neural networks work?"])
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Validate arguments and print the planned workflow without loading a model.")
    args = parser.parse_args()

    if args.dry_run:
        print("DRY RUN: would load SentenceTransformer:", args.model)
        print("DRY RUN: would encode corpus with encode_document and queries with encode_query")
        print("DRY RUN: queries:", args.query)
        print("DRY RUN: corpus size:", len(DEFAULT_CORPUS), "top_k:", min(args.top_k, len(DEFAULT_CORPUS)))
        return 0

    model = SentenceTransformer(args.model, local_files_only=args.local_files_only)
    corpus_embeddings = model.encode_document(DEFAULT_CORPUS, convert_to_tensor=True, normalize_embeddings=True)
    query_embeddings = model.encode_query(args.query, convert_to_tensor=True, normalize_embeddings=True)
    results = semantic_search(query_embeddings, corpus_embeddings, top_k=min(args.top_k, len(DEFAULT_CORPUS)))

    for query, hits in zip(args.query, results):
        print(f"Query: {query}")
        for hit in hits:
            print(f"{hit['score']:.4f}\t{DEFAULT_CORPUS[hit['corpus_id']]}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
