#!/usr/bin/env python
"""Smoke-test a SentenceTransformer model with a few local texts.

Examples:
    python dense_embedding_smoke.py
    python dense_embedding_smoke.py --model sentence-transformers/all-MiniLM-L6-v2 --local-files-only
"""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a minimal dense embedding smoke test.")
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--normalize", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(args.model, local_files_only=args.local_files_only)
    texts = [
        "The weather is lovely today.",
        "It is sunny outside.",
        "A database stores records.",
    ]
    embeddings = model.encode(
        texts,
        batch_size=args.batch_size,
        normalize_embeddings=args.normalize,
        convert_to_tensor=True,
    )
    scores = model.similarity(embeddings, embeddings)
    print(f"model: {args.model}")
    print(f"embedding shape: {tuple(embeddings.shape)}")
    print(f"similarity shape: {tuple(scores.shape)}")
    print(f"related score: {float(scores[0, 1]):.4f}")
    print(f"unrelated score: {float(scores[0, 2]):.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
