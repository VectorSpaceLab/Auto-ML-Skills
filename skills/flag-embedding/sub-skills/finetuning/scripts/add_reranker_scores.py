#!/usr/bin/env python3
"""Add FlagEmbedding reranker teacher scores to fine-tuning JSONL data.

This script loads a reranker model and can download checkpoints. Run it only
when the user asks to generate teacher scores.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def parse_devices(value: str | None) -> list[str] | None:
    if value is None:
        return None
    parts = [part.strip() for part in value.split(",") if part.strip()]
    return parts or None


def read_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, raw in enumerate(fh, start=1):
            if not raw.strip():
                continue
            row = json.loads(raw)
            if not isinstance(row, dict):
                raise ValueError(f"line {line_no}: expected JSON object")
            for key in ("query", "pos", "neg"):
                if key not in row:
                    raise ValueError(f"line {line_no}: missing {key!r}")
            rows.append(row)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--output_file", required=True)
    parser.add_argument("--reranker_name_or_path", required=True)
    parser.add_argument("--reranker_model_class", choices=["encoder-only-base", "decoder-only-base", "decoder-only-layerwise", "decoder-only-lightweight"])
    parser.add_argument("--reranker_peft_path")
    parser.add_argument("--devices", help="Comma-separated devices such as cuda:0,cuda:1 or cpu.")
    parser.add_argument("--cache_dir")
    parser.add_argument("--use_fp16", action="store_true")
    parser.add_argument("--use_bf16", action="store_true")
    parser.add_argument("--trust_remote_code", action="store_true")
    parser.add_argument("--query_instruction_for_rerank")
    parser.add_argument("--query_instruction_format_for_rerank", default="{}{}")
    parser.add_argument("--passage_instruction_for_rerank")
    parser.add_argument("--passage_instruction_format_for_rerank", default="{}{}")
    parser.add_argument("--reranker_batch_size", type=int, default=3000)
    parser.add_argument("--reranker_query_max_length", type=int)
    parser.add_argument("--reranker_max_length", type=int, default=512)
    parser.add_argument("--normalize", action="store_true")
    parser.add_argument("--prompt")
    parser.add_argument("--cutoff_layers", type=int, nargs="+")
    parser.add_argument("--compress_ratio", type=int, default=1)
    parser.add_argument("--compress_layers", type=int, nargs="+")
    args = parser.parse_args()

    try:
        from FlagEmbedding import FlagAutoReranker

        rows = read_rows(Path(args.input_file))
        reranker = FlagAutoReranker.from_finetuned(
            model_name_or_path=args.reranker_name_or_path,
            model_class=args.reranker_model_class,
            peft_path=args.reranker_peft_path,
            use_fp16=args.use_fp16,
            use_bf16=args.use_bf16,
            query_instruction_for_rerank=args.query_instruction_for_rerank,
            query_instruction_format=args.query_instruction_format_for_rerank,
            passage_instruction_for_rerank=args.passage_instruction_for_rerank,
            passage_instruction_format=args.passage_instruction_format_for_rerank,
            cache_dir=args.cache_dir,
            trust_remote_code=args.trust_remote_code,
            devices=parse_devices(args.devices),
            normalize=args.normalize,
            prompt=args.prompt,
            cutoff_layers=args.cutoff_layers,
            compress_layers=args.compress_layers,
            compress_ratio=args.compress_ratio,
            batch_size=args.reranker_batch_size,
            query_max_length=args.reranker_query_max_length,
            max_length=args.reranker_max_length,
        )

        pairs: list[tuple[str, str]] = []
        spans: list[tuple[int, int]] = []
        for row in rows:
            start = len(pairs)
            for text in row["pos"]:
                pairs.append((row["query"], text))
            for text in row["neg"]:
                pairs.append((row["query"], text))
            spans.append((start, len(pairs)))

        scores = reranker.compute_score(pairs)
        for row, (start, end) in zip(rows, spans):
            row_scores = [float(score) for score in scores[start:end]]
            pos_len = len(row["pos"])
            row["pos_scores"] = row_scores[:pos_len]
            row["neg_scores"] = row_scores[pos_len:]

        output = Path(args.output_file)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(json.dumps({"ok": True, "rows": len(rows), "pairs_scored": len(pairs), "output_file": str(output)}, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"}, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
