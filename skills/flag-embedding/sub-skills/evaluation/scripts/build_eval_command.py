#!/usr/bin/env python3
"""Print conservative FlagEmbedding evaluation command templates.

This prints a command; it does not run evaluation or download datasets.

Example:
    python scripts/build_eval_command.py --benchmark beir --dataset-dir ./beir/data --dataset-names fiqa arguana
"""

from __future__ import annotations

import argparse
import shlex


MODULES = {
    "mteb": "FlagEmbedding.evaluation.mteb",
    "beir": "FlagEmbedding.evaluation.beir",
    "msmarco": "FlagEmbedding.evaluation.msmarco",
    "miracl": "FlagEmbedding.evaluation.miracl",
    "mldr": "FlagEmbedding.evaluation.mldr",
    "mkqa": "FlagEmbedding.evaluation.mkqa",
    "bright": "FlagEmbedding.evaluation.bright",
    "custom": "FlagEmbedding.evaluation.custom",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", choices=MODULES, required=True)
    parser.add_argument("--dataset-dir", default=None)
    parser.add_argument("--dataset-names", nargs="*", default=None)
    parser.add_argument("--splits", nargs="+", default=["test"])
    parser.add_argument("--embedder", default="BAAI/bge-m3")
    parser.add_argument("--reranker", default=None)
    parser.add_argument("--devices", nargs="*", default=None)
    parser.add_argument("--output-root", default="./eval_outputs")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_prefix = f"{args.output_root.rstrip('/')}/{args.benchmark}"
    command = [
        "python",
        "-m",
        MODULES[args.benchmark],
        "--eval_name",
        args.benchmark,
        "--output_dir",
        f"{output_prefix}/search_results",
        "--search_top_k",
        "1000",
        "--rerank_top_k",
        "100",
        "--overwrite",
        "False",
        "--k_values",
        "10",
        "100",
        "--eval_output_method",
        "markdown",
        "--eval_output_path",
        f"{output_prefix}/eval_results.md",
        "--eval_metrics",
        "ndcg_at_10",
        "recall_at_100",
        "--embedder_name_or_path",
        args.embedder,
        "--cache_dir",
        "./cache/model",
    ]
    if args.dataset_dir:
        command.extend(["--dataset_dir", args.dataset_dir])
    if args.dataset_names:
        command.append("--dataset_names")
        command.extend(args.dataset_names)
    if args.splits:
        command.append("--splits")
        command.extend(args.splits)
    if args.reranker:
        command.extend(["--reranker_name_or_path", args.reranker])
    if args.devices:
        command.append("--devices")
        command.extend(args.devices)

    print(" ".join(shlex.quote(part) for part in command))


if __name__ == "__main__":
    main()
