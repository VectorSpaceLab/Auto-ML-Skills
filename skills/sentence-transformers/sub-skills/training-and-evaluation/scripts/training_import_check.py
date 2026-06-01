#!/usr/bin/env python
"""Check Sentence Transformers training imports without starting a training run."""

from __future__ import annotations

import importlib


def check_module(name: str) -> bool:
    try:
        importlib.import_module(name)
    except Exception as exc:
        print(f"{name}: missing or failed ({type(exc).__name__}: {exc})")
        return False
    print(f"{name}: ok")
    return True


def main() -> int:
    ok = True
    for module in ["datasets", "accelerate", "torch", "transformers", "sentence_transformers"]:
        ok = check_module(module) and ok

    try:
        from sentence_transformers import (
            CrossEncoderTrainer,
            CrossEncoderTrainingArguments,
            SentenceTransformerTrainer,
            SentenceTransformerTrainingArguments,
            SparseEncoderTrainer,
            SparseEncoderTrainingArguments,
        )
        from sentence_transformers.cross_encoder import losses as cross_losses
        from sentence_transformers.sentence_transformer import losses as dense_losses
        from sentence_transformers.sparse_encoder import losses as sparse_losses

        print("trainers: ok")
        print(f"dense loss sample: {dense_losses.MultipleNegativesRankingLoss.__name__}")
        print(f"cross loss sample: {cross_losses.BinaryCrossEntropyLoss.__name__}")
        print(f"sparse loss sample: {sparse_losses.SpladeLoss.__name__}")
        print(
            "arguments:",
            SentenceTransformerTrainingArguments.__name__,
            CrossEncoderTrainingArguments.__name__,
            SparseEncoderTrainingArguments.__name__,
        )
        print(
            "trainers:",
            SentenceTransformerTrainer.__name__,
            CrossEncoderTrainer.__name__,
            SparseEncoderTrainer.__name__,
        )
    except Exception as exc:
        print(f"training API import failed: {type(exc).__name__}: {exc}")
        ok = False

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
