#!/usr/bin/env python
"""Smoke-test a SparseEncoder with sparse encoding, sparsity, and token decode."""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a minimal SparseEncoder smoke test.")
    parser.add_argument("--model", default="naver/splade-cocondenser-ensembledistil")
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--max-active-dims", type=int, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    from sentence_transformers import SparseEncoder

    model = SparseEncoder(
        args.model,
        local_files_only=args.local_files_only,
        max_active_dims=args.max_active_dims,
    )
    texts = [
        "Neural networks learn representations.",
        "Mars rovers explore the planet.",
    ]
    embeddings = model.encode(texts, convert_to_sparse_tensor=True)
    print(f"model: {args.model}")
    print(f"embedding shape: {tuple(embeddings.shape)}")
    print(f"sparsity: {SparseEncoder.sparsity(embeddings)}")
    print(f"top tokens: {model.decode(embeddings[0], top_k=args.top_k)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
