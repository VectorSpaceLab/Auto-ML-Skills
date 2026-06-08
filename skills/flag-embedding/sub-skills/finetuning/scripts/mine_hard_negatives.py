#!/usr/bin/env python3
"""Mine hard negatives for FlagEmbedding fine-tuning JSONL data.

This script loads an embedder and FAISS. It can download checkpoints and use
GPU resources, so run it only when the user asks to generate mined negatives.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any

import numpy as np


def parse_devices(value: str | None) -> list[str] | None:
    if value is None:
        return None
    parts = [part.strip() for part in value.split(",") if part.strip()]
    return parts or None


def read_train_rows(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, raw in enumerate(fh, start=1):
            if not raw.strip():
                continue
            row = json.loads(raw)
            if not isinstance(row, dict):
                raise ValueError(f"line {line_no}: expected JSON object")
            for key in ("query", "pos"):
                if key not in row:
                    raise ValueError(f"line {line_no}: missing {key!r}")
            row.setdefault("neg", [])
            rows.append(row)
    return rows


def read_candidate_pool(path: Path) -> list[str]:
    corpus = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, raw in enumerate(fh, start=1):
            if not raw.strip():
                continue
            row = json.loads(raw)
            text = row.get("text") if isinstance(row, dict) else None
            if not isinstance(text, str):
                raise ValueError(f"candidate line {line_no}: missing text string")
            corpus.append(text)
    return corpus


def dense_array(value: Any) -> np.ndarray:
    if isinstance(value, dict):
        value = value.get("dense_vecs")
    return np.asarray(value, dtype=np.float32)


def create_index(embeddings: np.ndarray, use_gpu: bool):
    import faiss

    index = faiss.IndexFlatIP(embeddings.shape[1])
    if use_gpu:
        options = faiss.GpuMultipleClonerOptions()
        options.shard = True
        options.useFloat16 = True
        index = faiss.index_cpu_to_all_gpus(index, co=options)
    index.add(np.asarray(embeddings, dtype=np.float32))
    return index


def parse_sample_range(value: str) -> tuple[int, int]:
    left, right = value.split("-", 1)
    start, end = int(left), int(right)
    if start < 0 or end <= start:
        raise ValueError("--range_for_sampling must look like 2-200 with end > start >= 0")
    return start, end


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--output_file", required=True)
    parser.add_argument("--candidate_pool")
    parser.add_argument("--range_for_sampling", default="10-210")
    parser.add_argument("--negative_number", type=int, default=15)
    parser.add_argument("--use_gpu_for_searching", action="store_true")
    parser.add_argument("--search_batch_size", type=int, default=64)
    parser.add_argument("--embedder_name_or_path", required=True)
    parser.add_argument("--embedder_model_class", choices=["encoder-only-base", "encoder-only-m3", "decoder-only-base", "decoder-only-icl", "decoder-only-pseudo_moe"])
    parser.add_argument("--normalize_embeddings", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--pooling_method")
    parser.add_argument("--use_fp16", action="store_true")
    parser.add_argument("--devices", help="Comma-separated devices such as cuda:0,cuda:1 or cpu.")
    parser.add_argument("--query_instruction_for_retrieval")
    parser.add_argument("--query_instruction_format_for_retrieval", default="{}{}")
    parser.add_argument("--trust_remote_code", action="store_true")
    parser.add_argument("--cache_dir")
    parser.add_argument("--embedder_batch_size", type=int, default=3000)
    parser.add_argument("--embedder_query_max_length", type=int, default=512)
    parser.add_argument("--embedder_passage_max_length", type=int, default=512)
    parser.add_argument("--seed", type=int, default=13)
    args = parser.parse_args()

    try:
        from FlagEmbedding import FlagAutoModel

        random.seed(args.seed)
        rows = read_train_rows(Path(args.input_file))
        sample_start, sample_end = parse_sample_range(args.range_for_sampling)

        if args.candidate_pool:
            corpus = list(dict.fromkeys(read_candidate_pool(Path(args.candidate_pool))))
        else:
            corpus_values: list[str] = []
            for row in rows:
                corpus_values.extend(row["pos"])
                corpus_values.extend(row.get("neg", []))
            corpus = list(dict.fromkeys(corpus_values))
        if not corpus:
            raise ValueError("corpus is empty; provide positives/negatives or --candidate_pool")

        model = FlagAutoModel.from_finetuned(
            model_name_or_path=args.embedder_name_or_path,
            model_class=args.embedder_model_class,
            normalize_embeddings=args.normalize_embeddings,
            pooling_method=args.pooling_method,
            use_fp16=args.use_fp16,
            query_instruction_for_retrieval=args.query_instruction_for_retrieval,
            query_instruction_format=args.query_instruction_format_for_retrieval,
            devices=parse_devices(args.devices),
            trust_remote_code=args.trust_remote_code,
            cache_dir=args.cache_dir,
            batch_size=args.embedder_batch_size,
            query_max_length=args.embedder_query_max_length,
            passage_max_length=args.embedder_passage_max_length,
        )

        p_vecs = dense_array(model.encode(corpus))
        q_vecs = dense_array(model.encode_queries([row["query"] for row in rows]))
        topk = min(sample_end, len(corpus))
        index = create_index(p_vecs, args.use_gpu_for_searching)
        _, all_indices = index.search(np.asarray(q_vecs, dtype=np.float32), topk)

        for row, indices in zip(rows, all_indices.tolist()):
            positives = set(row["pos"])
            selected = []
            for idx in indices[sample_start:sample_end]:
                if idx == -1:
                    continue
                text = corpus[idx]
                if text not in positives and text != row["query"] and text not in selected:
                    selected.append(text)
                if len(selected) >= args.negative_number:
                    break
            while len(selected) < args.negative_number and corpus:
                candidate = random.choice(corpus)
                if candidate not in positives and candidate != row["query"] and candidate not in selected:
                    selected.append(candidate)
                if len(corpus) <= len(positives) + len(selected):
                    break
            row["neg"] = selected

        output = Path(args.output_file)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(json.dumps({"ok": True, "rows": len(rows), "corpus_size": len(corpus), "output_file": str(output)}, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"}, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
