#!/usr/bin/env python3
"""Build safe FlagEmbedding evaluation commands without executing them."""

from __future__ import annotations

import argparse
import json
import shlex
from pathlib import Path
from typing import Iterable


MODULES = {
    "beir": "FlagEmbedding.evaluation.beir",
    "mteb": "FlagEmbedding.evaluation.mteb",
    "miracl": "FlagEmbedding.evaluation.miracl",
    "mldr": "FlagEmbedding.evaluation.mldr",
    "mkqa": "FlagEmbedding.evaluation.mkqa",
    "msmarco": "FlagEmbedding.evaluation.msmarco",
    "air-bench": "FlagEmbedding.evaluation.air_bench",
    "air_bench": "FlagEmbedding.evaluation.air_bench",
    "bright": "FlagEmbedding.evaluation.bright",
    "custom": "FlagEmbedding.evaluation.custom",
}

DEFAULT_EVAL_NAMES = {
    "beir": "beir",
    "mteb": "mteb",
    "miracl": "miracl",
    "mldr": "mldr",
    "mkqa": "mkqa",
    "msmarco": "msmarco",
    "bright": "bright",
    "custom": "custom",
}

AIR_BENCH_KEYS = {"air-bench", "air_bench"}


def add_repeated(command: list[str], flag: str, values: Iterable[str] | None) -> None:
    if values:
        command.append(flag)
        command.extend(str(value) for value in values)


def add_optional(command: list[str], flag: str, value: object | None) -> None:
    if value is not None:
        command.extend([flag, str(value)])


def add_bool(command: list[str], flag: str, value: bool | None) -> None:
    if value is not None:
        command.extend([flag, "True" if value else "False"])


def shell_join(command: list[str]) -> str:
    return " \\\n  ".join(shlex.quote(part) for part in command)


def iter_jsonl(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            text = line.strip()
            if not text:
                continue
            try:
                value = json.loads(text)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSON in {path} line {line_number}: {exc}") from exc
            if not isinstance(value, dict):
                raise SystemExit(f"Expected JSON object in {path} line {line_number}")
            yield value


def validate_custom_dataset(dataset_dir: str, splits: list[str]) -> list[str]:
    root = Path(dataset_dir)
    warnings: list[str] = []
    if not root.exists():
        raise SystemExit(f"Custom dataset directory does not exist: {dataset_dir}")

    corpus_path = root / "corpus.jsonl"
    if not corpus_path.exists():
        raise SystemExit(f"Missing required custom dataset file: {corpus_path}")

    corpus_ids = set()
    for row in iter_jsonl(corpus_path):
        if "id" not in row or "text" not in row:
            raise SystemExit(f"Rows in {corpus_path} must contain 'id' and 'text'")
        corpus_ids.add(str(row["id"]))
    if not corpus_ids:
        warnings.append("corpus.jsonl has no records")

    for split in splits or ["test"]:
        queries_path = root / f"{split}_queries.jsonl"
        qrels_path = root / f"{split}_qrels.jsonl"
        if not queries_path.exists():
            raise SystemExit(f"Missing required custom dataset file: {queries_path}")
        if not qrels_path.exists():
            raise SystemExit(f"Missing required custom dataset file: {qrels_path}")

        query_ids = set()
        for row in iter_jsonl(queries_path):
            if "id" not in row or "text" not in row:
                raise SystemExit(f"Rows in {queries_path} must contain 'id' and 'text'")
            query_ids.add(str(row["id"]))

        missing_qids = set()
        missing_docids = set()
        for row in iter_jsonl(qrels_path):
            if "qid" not in row or "docid" not in row or "relevance" not in row:
                raise SystemExit(f"Rows in {qrels_path} must contain 'qid', 'docid', and 'relevance'")
            qid = str(row["qid"])
            docid = str(row["docid"])
            if qid not in query_ids:
                missing_qids.add(qid)
            if docid not in corpus_ids:
                missing_docids.add(docid)

        if missing_qids:
            preview = ", ".join(sorted(missing_qids)[:5])
            raise SystemExit(f"Qrels reference query ids missing from {queries_path}: {preview}")
        if missing_docids:
            preview = ", ".join(sorted(missing_docids)[:5])
            raise SystemExit(f"Qrels reference doc ids missing from {corpus_path}: {preview}")
        if not query_ids:
            warnings.append(f"{queries_path.name} has no records")

    return warnings


def build_command(args: argparse.Namespace) -> list[str]:
    benchmark = args.benchmark.lower()
    module = MODULES[benchmark]
    command = ["python", "-m", module]

    if benchmark in AIR_BENCH_KEYS:
        add_optional(command, "--benchmark_version", args.benchmark_version)
        add_repeated(command, "--task_types", args.task_types)
        add_repeated(command, "--domains", args.domains)
        add_repeated(command, "--languages", args.languages)
        add_repeated(command, "--splits", args.splits)
        add_optional(command, "--output_dir", args.output_dir)
        add_optional(command, "--search_top_k", args.search_top_k)
        add_optional(command, "--rerank_top_k", args.rerank_top_k)
        add_optional(command, "--cache_dir", args.cache_path)
        add_bool(command, "--overwrite", args.overwrite)
    else:
        eval_name = args.eval_name or DEFAULT_EVAL_NAMES.get(benchmark, benchmark)
        if benchmark == "bright" and not args.eval_name and args.task_type:
            eval_name = f"bright_{args.task_type}"
        add_optional(command, "--eval_name", eval_name)
        add_optional(command, "--dataset_dir", args.dataset_dir)
        add_repeated(command, "--dataset_names", args.dataset_names)
        add_repeated(command, "--splits", args.splits)
        add_optional(command, "--corpus_embd_save_dir", args.corpus_embd_save_dir)
        add_optional(command, "--output_dir", args.output_dir)
        add_optional(command, "--search_top_k", args.search_top_k)
        add_optional(command, "--rerank_top_k", args.rerank_top_k)
        add_optional(command, "--cache_path", args.cache_path)
        add_bool(command, "--force_redownload", args.force_redownload)
        add_bool(command, "--overwrite", args.overwrite)
        add_bool(command, "--ignore_identical_ids", args.ignore_identical_ids)
        add_repeated(command, "--k_values", args.k_values)
        add_optional(command, "--eval_output_method", args.eval_output_method)
        add_optional(command, "--eval_output_path", args.eval_output_path)
        add_repeated(command, "--eval_metrics", args.eval_metrics)

        if benchmark == "mteb":
            add_repeated(command, "--languages", args.languages)
            add_repeated(command, "--tasks", args.tasks)
            add_repeated(command, "--task_types", args.task_types)
            add_bool(command, "--use_special_instructions", args.use_special_instructions)
            add_optional(command, "--examples_path", args.examples_path)
        elif benchmark in {"beir", "bright"}:
            if benchmark == "bright":
                add_optional(command, "--task_type", args.task_type)
            add_bool(command, "--use_special_instructions", args.use_special_instructions)

    add_optional(command, "--embedder_name_or_path", args.embedder)
    add_optional(command, "--embedder_model_class", args.embedder_model_class)
    add_bool(command, "--normalize_embeddings", args.normalize_embeddings)
    add_optional(command, "--pooling_method", args.pooling_method)
    add_bool(command, "--use_fp16", args.use_fp16)
    add_bool(command, "--use_bf16", args.use_bf16)
    add_repeated(command, "--devices", args.devices)
    add_optional(command, "--query_instruction_for_retrieval", args.query_instruction_for_retrieval)
    add_optional(command, "--query_instruction_format_for_retrieval", args.query_instruction_format_for_retrieval)
    add_bool(command, "--trust_remote_code", args.trust_remote_code)
    add_optional(command, "--reranker_name_or_path", args.reranker)
    add_optional(command, "--reranker_model_class", args.reranker_model_class)
    add_optional(command, "--reranker_peft_path", args.reranker_peft_path)
    add_optional(command, "--query_instruction_for_rerank", args.query_instruction_for_rerank)
    add_optional(command, "--query_instruction_format_for_rerank", args.query_instruction_format_for_rerank)
    add_optional(command, "--passage_instruction_for_rerank", args.passage_instruction_for_rerank)
    add_optional(command, "--passage_instruction_format_for_rerank", args.passage_instruction_format_for_rerank)

    if benchmark in AIR_BENCH_KEYS:
        add_optional(command, "--model_cache_dir", args.model_cache_dir)
    else:
        add_optional(command, "--cache_dir", args.model_cache_dir)

    add_optional(command, "--embedder_batch_size", args.embedder_batch_size)
    add_optional(command, "--reranker_batch_size", args.reranker_batch_size)
    add_optional(command, "--embedder_query_max_length", args.embedder_query_max_length)
    add_optional(command, "--embedder_passage_max_length", args.embedder_passage_max_length)
    add_optional(command, "--truncate_dim", args.truncate_dim)
    add_optional(command, "--reranker_query_max_length", args.reranker_query_max_length)
    add_optional(command, "--reranker_max_length", args.reranker_max_length)
    add_bool(command, "--normalize", args.normalize)
    add_optional(command, "--prompt", args.prompt)
    add_repeated(command, "--cutoff_layers", args.cutoff_layers)
    add_optional(command, "--compress_ratio", args.compress_ratio)
    add_repeated(command, "--compress_layers", args.compress_layers)
    return command


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a FlagEmbedding evaluation command without executing it.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--benchmark", required=True, choices=sorted(MODULES), help="Benchmark family to target.")
    parser.add_argument("--execute-note", action="store_true", help="Print an extra warning that the command is not executed by this script.")

    parser.add_argument("--eval-name")
    parser.add_argument("--dataset-dir")
    parser.add_argument("--dataset-names", nargs="+")
    parser.add_argument("--splits", nargs="+", default=["test"])
    parser.add_argument("--corpus-embd-save-dir")
    parser.add_argument("--output-dir", default="./search_results")
    parser.add_argument("--search-top-k", type=int, default=1000)
    parser.add_argument("--rerank-top-k", type=int, default=100)
    parser.add_argument("--cache-path")
    parser.add_argument("--force-redownload", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--overwrite", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--ignore-identical-ids", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--k-values", nargs="+", default=["10", "100"])
    parser.add_argument("--eval-output-method", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--eval-output-path", default="./eval_results.md")
    parser.add_argument("--eval-metrics", nargs="+", default=["ndcg_at_10", "recall_at_100"])

    parser.add_argument("--languages", nargs="+")
    parser.add_argument("--tasks", nargs="+")
    parser.add_argument("--task-types", nargs="+")
    parser.add_argument("--domains", nargs="+")
    parser.add_argument("--benchmark-version", default="AIR-Bench_24.05")
    parser.add_argument("--task-type", choices=["short", "long"], default=None)
    parser.add_argument("--use-special-instructions", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--examples-path")

    parser.add_argument("--embedder", required=True, help="Value for --embedder_name_or_path.")
    parser.add_argument("--embedder-model-class")
    parser.add_argument("--normalize-embeddings", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--pooling-method")
    parser.add_argument("--use-fp16", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--use-bf16", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--devices", nargs="+")
    parser.add_argument("--query-instruction-for-retrieval")
    parser.add_argument("--query-instruction-format-for-retrieval")
    parser.add_argument("--trust-remote-code", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--reranker", help="Value for --reranker_name_or_path.")
    parser.add_argument("--reranker-model-class")
    parser.add_argument("--reranker-peft-path")
    parser.add_argument("--query-instruction-for-rerank")
    parser.add_argument("--query-instruction-format-for-rerank")
    parser.add_argument("--passage-instruction-for-rerank")
    parser.add_argument("--passage-instruction-format-for-rerank")
    parser.add_argument("--model-cache-dir")
    parser.add_argument("--embedder-batch-size", type=int)
    parser.add_argument("--reranker-batch-size", type=int)
    parser.add_argument("--embedder-query-max-length", type=int)
    parser.add_argument("--embedder-passage-max-length", type=int)
    parser.add_argument("--truncate-dim", type=int)
    parser.add_argument("--reranker-query-max-length", type=int)
    parser.add_argument("--reranker-max-length", type=int)
    parser.add_argument("--normalize", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--prompt")
    parser.add_argument("--cutoff-layers", nargs="+")
    parser.add_argument("--compress-ratio", type=int)
    parser.add_argument("--compress-layers", nargs="+")
    parser.add_argument("--validate-custom-data", action="store_true", help="For --benchmark custom, validate JSONL file presence and qrels ids before printing.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    benchmark = args.benchmark.lower()
    warnings: list[str] = []

    if benchmark == "custom":
        if not args.dataset_dir:
            raise SystemExit("--dataset-dir is required for --benchmark custom")
        if args.dataset_names:
            raise SystemExit("Do not pass --dataset-names for --benchmark custom; the custom loader has no dataset names")
        if args.validate_custom_data:
            warnings.extend(validate_custom_dataset(args.dataset_dir, args.splits))

    if benchmark == "mteb" and args.eval_output_method != "json":
        warnings.append("MTEB runner writes aggregate results as JSON; consider --eval-output-method json and a .json path.")

    if benchmark in AIR_BENCH_KEYS and args.cache_path:
        warnings.append("AIR-Bench maps --cache-path to AIR-Bench --cache_dir; model cache uses --model-cache-dir.")

    command = build_command(args)
    if args.execute_note:
        print("# This script only prints a command. It does not execute downloads or benchmarks.")
    for warning in warnings:
        print(f"# Warning: {warning}")
    print(shell_join(command))


if __name__ == "__main__":
    main()
