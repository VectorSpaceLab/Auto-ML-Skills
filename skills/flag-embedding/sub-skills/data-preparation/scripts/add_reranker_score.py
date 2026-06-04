#!/usr/bin/env python3
"""Add reranker teacher scores to FlagEmbedding training JSONL.

Example:
    python scripts/add_reranker_score.py \
      --input_file train_minedHN.jsonl \
      --output_file train_score.jsonl \
      --reranker_name_or_path BAAI/bge-reranker-v2-m3
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Optional

from transformers import HfArgumentParser


@dataclass
class ScoreArgs:
    input_file: str = field(metadata={"help": "Input JSONL with query, pos, and neg."})
    output_file: str = field(metadata={"help": "Output JSONL with pos_scores and neg_scores."})


@dataclass
class ModelArgs:
    use_fp16: bool = field(default=True)
    use_bf16: bool = field(default=False)
    devices: Optional[str] = field(default=None, metadata={"nargs": "+"})
    trust_remote_code: bool = field(default=False)
    reranker_name_or_path: Optional[str] = field(default=None)
    reranker_model_class: Optional[str] = field(
        default=None,
        metadata={
            "choices": ["encoder-only-base", "decoder-only-base", "decoder-only-layerwise", "decoder-only-lightweight"]
        },
    )
    reranker_peft_path: Optional[str] = field(default=None)
    query_instruction_for_rerank: Optional[str] = field(default=None)
    query_instruction_format_for_rerank: str = field(default="{}{}")
    passage_instruction_for_rerank: Optional[str] = field(default=None)
    passage_instruction_format_for_rerank: str = field(default="{}{}")
    cache_dir: Optional[str] = field(default=None)
    reranker_batch_size: int = field(default=3000)
    reranker_query_max_length: Optional[int] = field(default=None)
    reranker_max_length: int = field(default=512)
    normalize: bool = field(default=False)
    prompt: Optional[str] = field(default=None)
    cutoff_layers: Optional[list[int]] = field(default=None)
    compress_ratio: int = field(default=1)
    compress_layers: Optional[list[int]] = field(default=None, metadata={"nargs": "+"})

    def __post_init__(self) -> None:
        self.query_instruction_format_for_rerank = self.query_instruction_format_for_rerank.replace("\\n", "\n")
        self.passage_instruction_format_for_rerank = self.passage_instruction_format_for_rerank.replace("\\n", "\n")


def main(score_args: ScoreArgs, model_args: ModelArgs) -> None:
    from FlagEmbedding import FlagAutoReranker

    reranker = FlagAutoReranker.from_finetuned(
        model_name_or_path=model_args.reranker_name_or_path,
        model_class=model_args.reranker_model_class,
        peft_path=model_args.reranker_peft_path,
        use_fp16=model_args.use_fp16,
        use_bf16=model_args.use_bf16,
        query_instruction_for_rerank=model_args.query_instruction_for_rerank,
        query_instruction_format=model_args.query_instruction_format_for_rerank,
        passage_instruction_for_rerank=model_args.passage_instruction_for_rerank,
        passage_instruction_format=model_args.passage_instruction_format_for_rerank,
        cache_dir=model_args.cache_dir,
        trust_remote_code=model_args.trust_remote_code,
        devices=model_args.devices,
        normalize=model_args.normalize,
        prompt=model_args.prompt,
        cutoff_layers=model_args.cutoff_layers,
        compress_layers=model_args.compress_layers,
        compress_ratio=model_args.compress_ratio,
        batch_size=model_args.reranker_batch_size,
        query_max_length=model_args.reranker_query_max_length,
        max_length=model_args.reranker_max_length,
    )

    pairs = []
    rows = []
    with open(score_args.input_file, "r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            rows.append(row)
            for passage in row["pos"]:
                pairs.append((row["query"], passage))
            for passage in row["neg"]:
                pairs.append((row["query"], passage))

    scores = reranker.compute_score(pairs)
    idx = 0
    for row in rows:
        row["pos_scores"] = [float(scores[idx + i]) for i in range(len(row["pos"]))]
        idx += len(row["pos"])
        row["neg_scores"] = [float(scores[idx + i]) for i in range(len(row["neg"]))]
        idx += len(row["neg"])

    with open(score_args.output_file, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    parser = HfArgumentParser((ScoreArgs, ModelArgs))
    score_args, model_args = parser.parse_args_into_dataclasses()
    main(score_args, model_args)
