#!/usr/bin/env python3
"""Recommend common FlagEmbedding model_class values without importing FlagEmbedding."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import PurePosixPath


@dataclass(frozen=True)
class Recommendation:
    kind: str
    model_class: str
    auto_class: str
    pooling: str | None = None
    trust_remote_code: bool = False
    query_instruction_format: str | None = None
    note: str = ""


EMBEDDERS: dict[str, Recommendation] = {
    "bge-reasoner-embed-qwen3-8b-0923": Recommendation("embedder", "decoder-only-base", "FlagLLMModel", "last_token", False, "Instruct: {}\\nQuery: {}"),
    "bge-code-v1": Recommendation("embedder", "decoder-only-base", "FlagLLMModel", "last_token", True, "<instruct>{}\\n<query>{}"),
    "bge-en-icl": Recommendation("embedder", "decoder-only-icl", "FlagICLModel", "last_token", False, "<instruct>{}\\n<query>{}"),
    "bge-multilingual-gemma2": Recommendation("embedder", "decoder-only-base", "FlagLLMModel", "last_token", False, "<instruct>{}\\n<query>{}"),
    "bge-m3": Recommendation("embedder", "encoder-only-m3", "BGEM3FlagModel", "cls", False, None, "Supports dense, sparse, and multi-vector retrieval."),
    "Qwen3-Embedding-0.6B": Recommendation("embedder", "decoder-only-base", "FlagLLMModel", "last_token", False, "Instruct: {}\\nQuery:{}"),
    "Qwen3-Embedding-4B": Recommendation("embedder", "decoder-only-base", "FlagLLMModel", "last_token", False, "Instruct: {}\\nQuery:{}"),
    "Qwen3-Embedding-8B": Recommendation("embedder", "decoder-only-base", "FlagLLMModel", "last_token", False, "Instruct: {}\\nQuery:{}"),
    "e5-mistral-7b-instruct": Recommendation("embedder", "decoder-only-base", "FlagLLMModel", "last_token", False, "Instruct: {}\\nQuery: {}"),
    "multilingual-e5-large-instruct": Recommendation("embedder", "encoder-only-base", "FlagModel", "mean", False, "Instruct: {}\\nQuery: {}"),
    "gte-Qwen2-7B-instruct": Recommendation("embedder", "decoder-only-base", "FlagLLMModel", "last_token", True, "Instruct: {}\\nQuery: {}"),
    "gte-Qwen2-1.5B-instruct": Recommendation("embedder", "decoder-only-base", "FlagLLMModel", "last_token", True, "Instruct: {}\\nQuery: {}"),
    "gte-Qwen1.5-7B-instruct": Recommendation("embedder", "decoder-only-base", "FlagLLMModel", "last_token", True, "Instruct: {}\\nQuery: {}"),
    "gte-multilingual-base": Recommendation("embedder", "encoder-only-base", "FlagModel", "cls", True),
    "gte-large-en-v1.5": Recommendation("embedder", "encoder-only-base", "FlagModel", "cls", True),
    "gte-base-en-v1.5": Recommendation("embedder", "encoder-only-base", "FlagModel", "cls", True),
    "SFR-Embedding-2_R": Recommendation("embedder", "decoder-only-base", "FlagLLMModel", "last_token", False, "Instruct: {}\\nQuery: {}"),
    "SFR-Embedding-Mistral": Recommendation("embedder", "decoder-only-base", "FlagLLMModel", "last_token", False, "Instruct: {}\\nQuery: {}"),
    "Linq-Embed-Mistral": Recommendation("embedder", "decoder-only-base", "FlagLLMModel", "last_token", False, "Instruct: {}\\nQuery: {}"),
    "bce-embedding-base_v1": Recommendation("embedder", "encoder-only-base", "FlagModel", "cls"),
}

for size in ("large", "base", "small"):
    EMBEDDERS[f"bge-{size}-en-v1.5"] = Recommendation("embedder", "encoder-only-base", "FlagModel", "cls", False, "{}{}", "English retrieval instruction is commonly used for query encoding.")
    EMBEDDERS[f"bge-{size}-zh-v1.5"] = Recommendation("embedder", "encoder-only-base", "FlagModel", "cls", False, "{}{}", "Chinese retrieval instruction is commonly used for query encoding.")
    EMBEDDERS[f"bge-{size}-en"] = Recommendation("embedder", "encoder-only-base", "FlagModel", "cls", False, "{}{}", "English retrieval instruction is commonly used for query encoding.")
    EMBEDDERS[f"bge-{size}-zh"] = Recommendation("embedder", "encoder-only-base", "FlagModel", "cls", False, "{}{}", "Chinese retrieval instruction is commonly used for query encoding.")
    EMBEDDERS[f"e5-{size}-v2"] = Recommendation("embedder", "encoder-only-base", "FlagModel", "mean")
    EMBEDDERS[f"e5-{size}"] = Recommendation("embedder", "encoder-only-base", "FlagModel", "mean")
    EMBEDDERS[f"multilingual-e5-{size}"] = Recommendation("embedder", "encoder-only-base", "FlagModel", "mean")
    EMBEDDERS[f"gte-{size}"] = Recommendation("embedder", "encoder-only-base", "FlagModel", "mean")
    EMBEDDERS[f"gte-{size}-zh"] = Recommendation("embedder", "encoder-only-base", "FlagModel", "cls")

RERANKERS: dict[str, Recommendation] = {
    "bge-reranker-base": Recommendation("reranker", "encoder-only-base", "FlagReranker"),
    "bge-reranker-large": Recommendation("reranker", "encoder-only-base", "FlagReranker"),
    "bge-reranker-v2-m3": Recommendation("reranker", "encoder-only-base", "FlagReranker"),
    "bge-reranker-v2-gemma": Recommendation("reranker", "decoder-only-base", "FlagLLMReranker"),
    "bge-reranker-v2-minicpm-layerwise": Recommendation("reranker", "decoder-only-layerwise", "LayerWiseFlagLLMReranker", note="Supports cutoff layer controls."),
    "bge-reranker-v2.5-gemma2-lightweight": Recommendation("reranker", "decoder-only-lightweight", "LightWeightFlagLLMReranker", note="Supports cutoff layer and compression controls."),
    "jinaai/jina-reranker-v2-base-multilingual": Recommendation("reranker", "encoder-only-base", "FlagReranker"),
    "Alibaba-NLP/gte-multilingual-reranker-base": Recommendation("reranker", "encoder-only-base", "FlagReranker"),
    "maidalun1020/bce-reranker-base_v1": Recommendation("reranker", "encoder-only-base", "FlagReranker"),
    "jinaai/jina-reranker-v1-turbo-en": Recommendation("reranker", "encoder-only-base", "FlagReranker"),
}


def basename(model_name: str) -> str:
    cleaned = model_name.rstrip("/")
    if cleaned in EMBEDDERS or cleaned in RERANKERS:
        return cleaned
    return PurePosixPath(cleaned).name


def find_recommendation(model_name: str, kind: str) -> Recommendation | None:
    key = basename(model_name)
    if kind in {"embedder", "auto"} and key in EMBEDDERS:
        return EMBEDDERS[key]
    if kind in {"reranker", "auto"} and key in RERANKERS:
        return RERANKERS[key]
    lowered = key.lower()
    if kind in {"embedder", "auto"}:
        if "bge-m3" in lowered:
            return EMBEDDERS["bge-m3"]
        if "bge-en-icl" in lowered:
            return EMBEDDERS["bge-en-icl"]
        if "bge-multilingual-gemma2" in lowered:
            return EMBEDDERS["bge-multilingual-gemma2"]
        if "bge-" in lowered:
            return Recommendation("embedder", "encoder-only-base", "FlagModel", "cls", False, "{}{}", "Heuristic for BGE encoder-style custom checkpoint; verify the base model.")
        if "qwen" in lowered or "mistral" in lowered or "gemma" in lowered:
            return Recommendation("embedder", "decoder-only-base", "FlagLLMModel", "last_token", note="Heuristic for decoder-only embedding checkpoint; verify the base model.")
    if kind in {"reranker", "auto"}:
        if "layerwise" in lowered:
            return RERANKERS["bge-reranker-v2-minicpm-layerwise"]
        if "lightweight" in lowered:
            return RERANKERS["bge-reranker-v2.5-gemma2-lightweight"]
        if "reranker" in lowered and ("gemma" in lowered or "llm" in lowered):
            return RERANKERS["bge-reranker-v2-gemma"]
        if "reranker" in lowered:
            return Recommendation("reranker", "encoder-only-base", "FlagReranker", note="Heuristic for encoder-only reranker checkpoint; verify the base model.")
    return None


def print_recommendation(model_name: str, recommendation: Recommendation | None) -> int:
    if recommendation is None:
        print(f"model: {model_name}")
        print("status: unknown")
        print("next_step: identify the base model family and pass model_class explicitly")
        return 1
    print(f"model: {model_name}")
    print(f"kind: {recommendation.kind}")
    print(f"model_class: {recommendation.model_class}")
    print(f"auto_class: {recommendation.auto_class}")
    if recommendation.pooling:
        print(f"pooling: {recommendation.pooling}")
    print(f"trust_remote_code: {str(recommendation.trust_remote_code).lower()}")
    if recommendation.query_instruction_format:
        print(f"query_instruction_format: {recommendation.query_instruction_format}")
    if recommendation.note:
        print(f"note: {recommendation.note}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Recommend common FlagEmbedding model_class values.")
    parser.add_argument("model_name", help="Model id, local checkpoint name, or path-like basename.")
    parser.add_argument("--kind", choices=("auto", "embedder", "reranker"), default="auto", help="Limit lookup to an embedder or reranker mapping.")
    args = parser.parse_args()
    return print_recommendation(args.model_name, find_recommendation(args.model_name, args.kind))


if __name__ == "__main__":
    raise SystemExit(main())
