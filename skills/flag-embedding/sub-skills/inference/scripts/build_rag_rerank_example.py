#!/usr/bin/env python3
"""Small retrieval + reranking example template.

This script downloads models when run with real Hugging Face model names. Use it
as an adaptation template after the user has chosen models and allowed downloads.

Example:
    python sub-skills/inference/scripts/build_rag_rerank_example.py \
      --embedder BAAI/bge-base-en-v1.5 \
      --reranker BAAI/bge-reranker-v2-m3 \
      --device cuda:0
"""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--embedder", default="BAAI/bge-base-en-v1.5")
    parser.add_argument("--reranker", default="BAAI/bge-reranker-v2-m3")
    parser.add_argument("--device", default=None)
    parser.add_argument("--query", default="what is FlagEmbedding?")
    parser.add_argument(
        "--passage",
        action="append",
        default=[
            "FlagEmbedding is a retrieval toolkit for embeddings, reranking, fine-tuning, and evaluation.",
            "A cooking recipe lists ingredients and preparation steps.",
        ],
    )
    parser.add_argument("--top-k", type=int, default=2)
    parser.add_argument("--use-fp16", action="store_true")
    return parser.parse_args()


def main() -> None:
    from FlagEmbedding import FlagAutoModel, FlagAutoReranker

    args = parse_args()
    devices = [args.device] if args.device else None

    embedder = FlagAutoModel.from_finetuned(
        args.embedder,
        query_instruction_for_retrieval="Represent this sentence for searching relevant passages: ",
        devices=devices,
        use_fp16=args.use_fp16,
    )
    q = embedder.encode_queries([args.query])
    p = embedder.encode_corpus(args.passage)
    if isinstance(q, dict):
        q = q["dense_vecs"]
    if isinstance(p, dict):
        p = p["dense_vecs"]

    scores = (q @ p.T)[0]
    ranked = sorted(enumerate(scores), key=lambda item: float(item[1]), reverse=True)[: args.top_k]
    pairs = [[args.query, args.passage[i]] for i, _ in ranked]

    reranker = FlagAutoReranker.from_finetuned(args.reranker, devices=devices, use_fp16=args.use_fp16)
    rerank_scores = reranker.compute_score(pairs)
    for (idx, dense_score), rerank_score in zip(ranked, rerank_scores):
        print({"passage": args.passage[idx], "dense_score": float(dense_score), "rerank_score": float(rerank_score)})


if __name__ == "__main__":
    main()
