#!/usr/bin/env python
"""Dense retrieve then CrossEncoder rerank over a tiny local corpus.

This is a compact template for retrieve-and-rerank control flow. It may
download the selected models unless they are cached or --local-files-only is set.
"""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a small dense retrieve + cross rerank example.")
    parser.add_argument("--retriever", default="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
    parser.add_argument("--reranker", default="cross-encoder/ms-marco-MiniLM-L6-v2")
    parser.add_argument("--candidate-k", type=int, default=4)
    parser.add_argument("--final-k", type=int, default=3)
    parser.add_argument("--local-files-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    from sentence_transformers import CrossEncoder, SentenceTransformer
    from sentence_transformers.util import dot_score, semantic_search

    corpus = [
        "Python is a programming language used for automation and data science.",
        "Mars is known as the Red Planet.",
        "Berlin is the capital of Germany and has millions of residents.",
        "Vector databases store embeddings for similarity search.",
        "The Moon orbits Earth.",
    ]
    query = "What database stores embeddings?"

    retriever = SentenceTransformer(args.retriever, local_files_only=args.local_files_only)
    corpus_embeddings = retriever.encode_document(corpus, normalize_embeddings=True, convert_to_tensor=True)
    query_embeddings = retriever.encode_query([query], normalize_embeddings=True, convert_to_tensor=True)
    dense_hits = semantic_search(
        query_embeddings,
        corpus_embeddings,
        top_k=min(args.candidate_k, len(corpus)),
        score_function=dot_score,
    )[0]

    candidate_ids = [hit["corpus_id"] for hit in dense_hits]
    candidates = [corpus[i] for i in candidate_ids]

    reranker = CrossEncoder(args.reranker, local_files_only=args.local_files_only)
    ranks = reranker.rank(query, candidates, top_k=min(args.final_k, len(candidates)))

    print(f"Query: {query}")
    for row in ranks:
        original_id = candidate_ids[row["corpus_id"]]
        print(f"{row['score']:.4f}\tcorpus_id={original_id}\t{corpus[original_id]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
