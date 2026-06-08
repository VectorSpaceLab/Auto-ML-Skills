#!/usr/bin/env python3
"""
Self-contained CrossEncoder reranking example.

Example:
  python rerank_candidates.py --query "Which planet is the Red Planet?"
"""

from __future__ import annotations

import argparse

from sentence_transformers import CrossEncoder


DEFAULT_PASSAGES = [
    "Venus is often called Earth's twin because of its similar size and proximity.",
    "Mars is known for its reddish appearance and is often called the Red Planet.",
    "Jupiter is the largest planet in the solar system and has a prominent red spot.",
    "Saturn is famous for its rings.",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="cross-encoder/ms-marco-MiniLM-L6-v2")
    parser.add_argument("--query", default="Which planet is known as the Red Planet?")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Validate arguments and print the planned workflow without loading a model.")
    args = parser.parse_args()

    if args.dry_run:
        print("DRY RUN: would load CrossEncoder:", args.model)
        print("DRY RUN: would rerank", len(DEFAULT_PASSAGES), "candidate passages for query:", args.query)
        print("DRY RUN: top_k:", min(args.top_k, len(DEFAULT_PASSAGES)))
        return 0

    model = CrossEncoder(args.model, local_files_only=args.local_files_only)
    ranks = model.rank(args.query, DEFAULT_PASSAGES, top_k=min(args.top_k, len(DEFAULT_PASSAGES)), return_documents=True)

    print(f"Query: {args.query}")
    for row in ranks:
        print(f"{row['score']:.4f}\t#{row['corpus_id']}\t{row['text']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
