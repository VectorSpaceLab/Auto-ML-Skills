#!/usr/bin/env python3
"""Mine hard negatives for FlagEmbedding training data.

Self-contained adaptation of the FlagEmbedding helper script. It loads an
embedder, embeds queries and candidate passages, searches with FAISS inner
product, and writes JSONL with sampled `neg` values.

Example:
    python scripts/hn_mine.py \
      --input_file train.jsonl \
      --output_file train_minedHN.jsonl \
      --range_for_sampling 2-200 \
      --negative_number 15 \
      --embedder_name_or_path BAAI/bge-base-en-v1.5
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from tqdm import tqdm
from transformers import HfArgumentParser


@dataclass
class DataArgs:
    input_file: str = field(metadata={"help": "Input training JSONL."})
    output_file: str = field(metadata={"help": "Output JSONL with mined negatives."})
    candidate_pool: Optional[str] = field(default=None, metadata={"help": "Optional JSONL with a 'text' field."})
    range_for_sampling: str = field(default="10-210", metadata={"help": "Rank range to sample negatives from, e.g. 2-200."})
    negative_number: int = field(default=15, metadata={"help": "Number of negatives per query."})
    use_gpu_for_searching: bool = field(default=False, metadata={"help": "Use FAISS GPU search."})
    search_batch_size: int = field(default=64, metadata={"help": "FAISS search batch size."})


@dataclass
class ModelArgs:
    embedder_name_or_path: str = field(metadata={"help": "Embedder model or path.", "required": True})
    embedder_model_class: Optional[str] = field(
        default=None,
        metadata={
            "help": "Embedder class for custom models.",
            "choices": ["encoder-only-base", "encoder-only-m3", "decoder-only-base", "decoder-only-icl", "decoder-only-pseudo_moe"],
        },
    )
    normalize_embeddings: bool = field(default=True)
    pooling_method: Optional[str] = field(default=None)
    use_fp16: bool = field(default=True)
    use_bf16: bool = field(default=False)
    devices: Optional[str] = field(default=None, metadata={"nargs": "+"})
    query_instruction_for_retrieval: Optional[str] = field(default=None)
    query_instruction_format_for_retrieval: str = field(default="{}{}")
    examples_for_task: Optional[str] = field(default=None)
    examples_instruction_format: str = field(default="{}{}")
    trust_remote_code: bool = field(default=False)
    cache_dir: Optional[str] = field(default=None)
    embedder_batch_size: int = field(default=3000)
    embedder_query_max_length: int = field(default=512)
    embedder_passage_max_length: int = field(default=512)

    def __post_init__(self) -> None:
        self.query_instruction_format_for_retrieval = self.query_instruction_format_for_retrieval.replace("\\n", "\n")
        self.examples_instruction_format = self.examples_instruction_format.replace("\\n", "\n")


def read_jsonl(path: str) -> list[dict]:
    rows = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def get_corpus(candidate_pool: str) -> list[str]:
    corpus = []
    with open(candidate_pool, "r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            corpus.append(row["text"])
    return corpus


def create_index(embeddings: np.ndarray, use_gpu: bool = False):
    import faiss

    embeddings = np.asarray(embeddings, dtype=np.float32)
    index = faiss.IndexFlatIP(len(embeddings[0]))
    if use_gpu:
        options = faiss.GpuMultipleClonerOptions()
        options.shard = True
        options.useFloat16 = True
        index = faiss.index_cpu_to_all_gpus(index, co=options)
    index.add(embeddings)
    return index


def batch_search(index, query: np.ndarray, topk: int, batch_size: int) -> list[list[int]]:
    all_indices: list[list[int]] = []
    for start in tqdm(range(0, len(query), batch_size), desc="search batches", disable=len(query) < 256):
        batch = np.asarray(query[start : start + batch_size], dtype=np.float32)
        _, indices = index.search(batch, k=topk)
        all_indices.extend(indices.tolist())
    return all_indices


def load_model(args: ModelArgs):
    from FlagEmbedding import FlagAutoModel

    return FlagAutoModel.from_finetuned(
        model_name_or_path=args.embedder_name_or_path,
        model_class=args.embedder_model_class,
        normalize_embeddings=args.normalize_embeddings,
        pooling_method=args.pooling_method,
        use_fp16=args.use_fp16,
        use_bf16=args.use_bf16,
        query_instruction_for_retrieval=args.query_instruction_for_retrieval,
        query_instruction_format=args.query_instruction_format_for_retrieval,
        devices=args.devices,
        examples_for_task=args.examples_for_task,
        examples_instruction_format=args.examples_instruction_format,
        trust_remote_code=args.trust_remote_code,
        cache_dir=args.cache_dir,
        batch_size=args.embedder_batch_size,
        query_max_length=args.embedder_query_max_length,
        passage_max_length=args.embedder_passage_max_length,
    )


def parse_range(value: str) -> tuple[int, int]:
    left, right = value.split("-", 1)
    start, stop = int(left), int(right)
    if start < 0 or stop <= start:
        raise ValueError("--range_for_sampling must be like 2-200 with 0 <= start < stop")
    return start, stop


def main(data_args: DataArgs, model_args: ModelArgs) -> None:
    sample_start, sample_stop = parse_range(data_args.range_for_sampling)
    train_data = read_jsonl(data_args.input_file)
    corpus: list[str] = []
    queries: list[str] = []
    for row in train_data:
        corpus.extend(row["pos"])
        corpus.extend(row.get("neg", []))
        queries.append(row["query"])

    if data_args.candidate_pool is not None:
        corpus = get_corpus(data_args.candidate_pool)
    corpus = list(dict.fromkeys(corpus))
    if len(corpus) < data_args.negative_number:
        raise SystemExit("Corpus is too small for requested negative_number.")

    model = load_model(model_args)
    print(f"Encoding corpus: {len(corpus)}")
    p_vecs = model.encode(corpus)
    print(f"Encoding queries: {len(queries)}")
    q_vecs = model.encode_queries(queries)
    if isinstance(p_vecs, dict):
        p_vecs = p_vecs["dense_vecs"]
    if isinstance(q_vecs, dict):
        q_vecs = q_vecs["dense_vecs"]

    topk = min(sample_stop, len(corpus))
    index = create_index(p_vecs, use_gpu=data_args.use_gpu_for_searching)
    all_indices = batch_search(index, q_vecs, topk=topk, batch_size=data_args.search_batch_size)

    for row, indices in zip(train_data, all_indices):
        positives = set(row["pos"])
        query = row["query"]
        candidates = []
        for idx in indices[sample_start:sample_stop]:
            if idx == -1:
                break
            text = corpus[idx]
            if text not in positives and text != query:
                candidates.append(text)
        if len(candidates) > data_args.negative_number:
            candidates = random.sample(candidates, data_args.negative_number)
        if len(candidates) < data_args.negative_number:
            fallback = [text for text in corpus if text not in positives and text != query and text not in candidates]
            candidates.extend(random.sample(fallback, min(len(fallback), data_args.negative_number - len(candidates))))
        row["neg"] = candidates

    with open(data_args.output_file, "w", encoding="utf-8") as handle:
        for row in train_data:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    parser = HfArgumentParser((DataArgs, ModelArgs))
    data_args, model_args = parser.parse_args_into_dataclasses()
    main(data_args, model_args)
