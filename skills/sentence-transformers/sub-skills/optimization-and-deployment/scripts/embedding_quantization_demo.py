#!/usr/bin/env python
"""Demonstrate encode-time embedding quantization on a tiny text list."""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare float and quantized embedding shapes/dtypes.")
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--precision", choices=["int8", "uint8", "binary", "ubinary"], default="int8")
    parser.add_argument("--local-files-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    from sentence_transformers import SentenceTransformer

    texts = [
        "Vector search uses embeddings.",
        "Cross Encoders rerank candidate documents.",
        "Sparse encoders produce mostly zero dimensions.",
    ]
    model = SentenceTransformer(args.model, local_files_only=args.local_files_only)
    float_embeddings = model.encode(texts, precision="float32")
    quantized_embeddings = model.encode(texts, precision=args.precision)
    print(f"model: {args.model}")
    print(f"float32: shape={float_embeddings.shape}, dtype={float_embeddings.dtype}")
    print(f"{args.precision}: shape={quantized_embeddings.shape}, dtype={quantized_embeddings.dtype}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
