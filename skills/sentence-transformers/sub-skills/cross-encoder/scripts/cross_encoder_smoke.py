#!/usr/bin/env python
"""Smoke-test a CrossEncoder by ranking a tiny in-memory passage list."""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a minimal CrossEncoder ranking smoke test.")
    parser.add_argument("--model", default="cross-encoder/ms-marco-MiniLM-L6-v2")
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--sigmoid", action="store_true", help="Apply sigmoid to binary logits.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    from sentence_transformers import CrossEncoder

    activation_fn = None
    if args.sigmoid:
        import torch

        activation_fn = torch.nn.Sigmoid()

    model = CrossEncoder(args.model, local_files_only=args.local_files_only)
    query = "Which planet is known as the Red Planet?"
    passages = [
        "Mars is known for its reddish appearance and is often called the Red Planet.",
        "Venus is similar in size to Earth.",
        "Python is a programming language.",
    ]
    ranks = model.rank(
        query,
        passages,
        batch_size=args.batch_size,
        activation_fn=activation_fn,
        return_documents=True,
    )
    print(f"model: {args.model}")
    for row in ranks:
        print(f"{row['score']:.4f}\t#{row['corpus_id']}\t{row['text']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
