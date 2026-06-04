#!/usr/bin/env python
"""Tiny dense training skeleton for API validation and adaptation.

This script intentionally uses two toy examples and is not meant to produce a
useful model. It may download the selected base model unless cached or
--local-files-only is provided.
"""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a tiny SentenceTransformer training skeleton.")
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--output-dir", default="models/minimal-dense-training")
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--max-steps", type=int, default=1)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    from datasets import Dataset
    from sentence_transformers import SentenceTransformer, SentenceTransformerTrainer, SentenceTransformerTrainingArguments
    from sentence_transformers.sentence_transformer import losses

    train_dataset = Dataset.from_dict(
        {
            "anchor": ["What is Python?", "What is Mars?"],
            "positive": ["Python is a programming language.", "Mars is the Red Planet."],
        }
    )
    model = SentenceTransformer(args.model, local_files_only=args.local_files_only)
    loss = losses.MultipleNegativesRankingLoss(model)
    train_args = SentenceTransformerTrainingArguments(
        output_dir=args.output_dir,
        max_steps=args.max_steps,
        per_device_train_batch_size=2,
        learning_rate=2e-5,
        logging_steps=1,
        save_strategy="no",
        report_to="none",
    )
    trainer = SentenceTransformerTrainer(model=model, args=train_args, train_dataset=train_dataset, loss=loss)
    trainer.train()
    model.save_pretrained(args.output_dir)
    print(f"saved: {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
