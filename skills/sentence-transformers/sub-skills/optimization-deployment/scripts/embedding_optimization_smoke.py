#!/usr/bin/env python3
"""
Smoke-test output embedding quantization and truncation.

This avoids model export and service dependencies. It downloads the requested
model unless it is cached or --local-files-only is set.
"""

from __future__ import annotations

import argparse

from sentence_transformers.util import truncate_embeddings
from sentence_transformers.util.quantization import quantize_embeddings


TEXTS = [
    "The weather is lovely today.",
    "It is sunny outside.",
    "A rover explores Mars.",
    "Renewable energy includes wind and solar power.",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--precision", choices=["int8", "uint8", "binary", "ubinary"], default="int8")
    parser.add_argument("--truncate-dim", type=int)
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument(
        "--synthetic",
        action="store_true",
        help="Use deterministic synthetic embeddings instead of loading a model. This is the no-download smoke-test path.",
    )
    args = parser.parse_args()

    if args.synthetic:
        import numpy as np

        rng = np.random.default_rng(13)
        embeddings = rng.normal(size=(len(TEXTS), 32)).astype("float32")
    else:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(args.model, local_files_only=args.local_files_only)
        embeddings = model.encode(TEXTS)
    print(f"float32 shape={embeddings.shape} dtype={embeddings.dtype}")

    quantized = quantize_embeddings(embeddings, precision=args.precision, calibration_embeddings=embeddings)
    print(f"{args.precision} shape={quantized.shape} dtype={quantized.dtype}")

    if args.truncate_dim:
        truncated = truncate_embeddings(embeddings, args.truncate_dim)
        print(f"truncated shape={truncated.shape} dtype={truncated.dtype}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
