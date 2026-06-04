#!/usr/bin/env python3
"""Build conservative FlagEmbedding torchrun command templates.

This prints a command; it does not run training.

Example:
    python scripts/build_training_command.py --workflow embedder-base --train-data ./train.jsonl --output-dir ./outputs/test
"""

from __future__ import annotations

import argparse
import shlex


WORKFLOWS = {
    "embedder-base": {
        "module": "FlagEmbedding.finetune.embedder.encoder_only.base",
        "model": "BAAI/bge-base-en-v1.5",
        "extra": [
            "--query_instruction_for_retrieval",
            "Represent this sentence for searching relevant passages: ",
            "--query_instruction_format",
            "{}{}",
            "--sentence_pooling_method",
            "cls",
            "--normalize_embeddings",
            "True",
            "--kd_loss_type",
            "kl_div",
        ],
    },
    "embedder-m3": {
        "module": "FlagEmbedding.finetune.embedder.encoder_only.m3",
        "model": "BAAI/bge-m3",
        "extra": [
            "--sentence_pooling_method",
            "cls",
            "--normalize_embeddings",
            "True",
            "--kd_loss_type",
            "m3_kd_loss",
            "--unified_finetuning",
            "True",
        ],
    },
    "reranker-base": {
        "module": "FlagEmbedding.finetune.reranker.encoder_only.base",
        "model": "BAAI/bge-reranker-base",
        "extra": [],
    },
    "reranker-llm": {
        "module": "FlagEmbedding.finetune.reranker.decoder_only.base",
        "model": "BAAI/bge-reranker-v2-gemma",
        "extra": [
            "--use_lora",
            "True",
            "--lora_rank",
            "32",
            "--lora_alpha",
            "64",
            "--target_modules",
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "--save_merged_lora_model",
            "True",
            "--model_type",
            "decoder",
            "--query_instruction_for_rerank",
            "A: ",
            "--passage_instruction_for_rerank",
            "B: ",
        ],
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow", choices=WORKFLOWS, required=True)
    parser.add_argument("--train-data", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model-name-or-path", default=None)
    parser.add_argument("--cache-dir", default="./cache/model")
    parser.add_argument("--cache-path", default="./cache/data")
    parser.add_argument("--nproc-per-node", type=int, default=1)
    parser.add_argument("--deepspeed", default=None)
    parser.add_argument("--knowledge-distillation", choices=["True", "False"], default="False")
    parser.add_argument("--precision", choices=["none", "fp16", "bf16"], default="none")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workflow = WORKFLOWS[args.workflow]
    command = [
        "torchrun",
        "--nproc_per_node",
        str(args.nproc_per_node),
        "-m",
        workflow["module"],
        "--model_name_or_path",
        args.model_name_or_path or workflow["model"],
        "--cache_dir",
        args.cache_dir,
        "--train_data",
        args.train_data,
        "--cache_path",
        args.cache_path,
        "--train_group_size",
        "8",
        "--query_max_len",
        "512",
        "--passage_max_len",
        "512",
        "--pad_to_multiple_of",
        "8",
        "--knowledge_distillation",
        args.knowledge_distillation,
        "--output_dir",
        args.output_dir,
        "--overwrite_output_dir",
        "--learning_rate",
        "1e-5",
        "--num_train_epochs",
        "1",
        "--per_device_train_batch_size",
        "2",
        "--dataloader_drop_last",
        "True",
        "--logging_steps",
        "10",
        "--save_steps",
        "500",
    ]
    if args.precision != "none":
        command.append(f"--{args.precision}")
    if args.deepspeed:
        command.extend(["--deepspeed", args.deepspeed])
    command.extend(workflow["extra"])

    print(" ".join(shlex.quote(part) for part in command))


if __name__ == "__main__":
    main()
