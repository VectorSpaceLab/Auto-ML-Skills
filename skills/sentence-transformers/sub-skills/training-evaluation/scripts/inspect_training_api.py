#!/usr/bin/env python3
"""
Print available sentence-transformers training classes and key signatures.

This is a read-only helper for agents adapting training code to the installed
package version.
"""

from __future__ import annotations

import inspect


def show(name: str, obj: object) -> None:
    try:
        signature = inspect.signature(obj)
    except Exception as exc:  # pragma: no cover - diagnostic path.
        signature = f"<signature unavailable: {exc}>"
    print(f"{name}: {signature}")


def main() -> int:
    from sentence_transformers import SentenceTransformerTrainer, SentenceTransformerTrainingArguments
    from sentence_transformers.cross_encoder.trainer import CrossEncoderTrainer
    from sentence_transformers.cross_encoder.training_args import CrossEncoderTrainingArguments
    from sentence_transformers.sparse_encoder.trainer import SparseEncoderTrainer
    from sentence_transformers.sparse_encoder.training_args import SparseEncoderTrainingArguments

    objects = {
        "SentenceTransformerTrainer": SentenceTransformerTrainer.__init__,
        "SentenceTransformerTrainingArguments": SentenceTransformerTrainingArguments.__init__,
        "CrossEncoderTrainer": CrossEncoderTrainer.__init__,
        "CrossEncoderTrainingArguments": CrossEncoderTrainingArguments.__init__,
        "SparseEncoderTrainer": SparseEncoderTrainer.__init__,
        "SparseEncoderTrainingArguments": SparseEncoderTrainingArguments.__init__,
    }
    for name, obj in objects.items():
        show(name, obj)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
