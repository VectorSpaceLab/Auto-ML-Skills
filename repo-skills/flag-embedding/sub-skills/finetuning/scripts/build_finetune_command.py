#!/usr/bin/env python3
"""Print FlagEmbedding fine-tuning commands without executing them."""

from __future__ import annotations

import argparse
import shlex
import sys
from pathlib import Path

FAMILIES = {
    "embedder-encoder-base": {
        "module": "FlagEmbedding.finetune.embedder.encoder_only.base",
        "kind": "embedder",
        "default_model": "BAAI/bge-large-en-v1.5",
        "pooling": "cls",
        "kd_loss": "kl_div",
        "precision": "fp16",
    },
    "embedder-m3": {
        "module": "FlagEmbedding.finetune.embedder.encoder_only.m3",
        "kind": "embedder",
        "default_model": "BAAI/bge-m3",
        "pooling": "cls",
        "kd_loss": "m3_kd_loss",
        "precision": "fp16",
    },
    "embedder-decoder-base": {
        "module": "FlagEmbedding.finetune.embedder.decoder_only.base",
        "kind": "embedder",
        "default_model": "BAAI/bge-multilingual-gemma2",
        "pooling": "last_token",
        "kd_loss": "m3_kd_loss",
        "precision": "fp16",
    },
    "embedder-decoder-icl": {
        "module": "FlagEmbedding.finetune.embedder.decoder_only.icl",
        "kind": "embedder",
        "default_model": "BAAI/bge-en-icl",
        "pooling": "last_token",
        "kd_loss": "kl_div",
        "precision": "fp16",
    },
    "reranker-encoder-base": {
        "module": "FlagEmbedding.finetune.reranker.encoder_only.base",
        "kind": "reranker",
        "default_model": "BAAI/bge-reranker-base",
        "precision": "fp16",
    },
    "reranker-decoder-base": {
        "module": "FlagEmbedding.finetune.reranker.decoder_only.base",
        "kind": "reranker",
        "default_model": "BAAI/bge-reranker-v2-gemma",
        "precision": "bf16",
    },
    "reranker-decoder-layerwise": {
        "module": "FlagEmbedding.finetune.reranker.decoder_only.layerwise",
        "kind": "reranker",
        "default_model": "BAAI/bge-reranker-v2-minicpm-layerwise",
        "precision": "bf16",
    },
}


def str_bool(value: str) -> bool:
    lowered = value.lower()
    if lowered in {"true", "1", "yes", "y"}:
        return True
    if lowered in {"false", "0", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError(f"expected true/false, got {value!r}")


def add_bool_arg(parser: argparse.ArgumentParser, name: str, default: bool | None = None, help_text: str = "") -> None:
    parser.add_argument(name, type=str_bool, default=default, metavar="true|false", help=help_text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family", choices=sorted(FAMILIES), required=True)
    parser.add_argument("--model-name-or-path", help="Checkpoint or local model path. Defaults by family.")
    parser.add_argument("--train-data", nargs="+", required=True, help="One or more JSONL files or directories.")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--cache-dir")
    parser.add_argument("--cache-path")
    parser.add_argument("--deepspeed", help="DeepSpeed JSON config path. Must exist before execution.")
    parser.add_argument("--nproc-per-node", type=int, default=1)
    parser.add_argument("--precision", choices=("fp16", "bf16", "none"), help="Precision flag to add.")
    parser.add_argument("--num-train-epochs", type=float, default=1.0)
    parser.add_argument("--learning-rate", default=None)
    parser.add_argument("--per-device-train-batch-size", type=int, default=2)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=1)
    parser.add_argument("--warmup-ratio", type=float, default=0.1)
    parser.add_argument("--weight-decay", type=float)
    parser.add_argument("--logging-steps", type=int, default=10)
    parser.add_argument("--save-steps", type=int, default=1000)
    parser.add_argument("--max-steps", type=int)
    parser.add_argument("--query-max-len", type=int, default=512)
    parser.add_argument("--passage-max-len", type=int, default=512)
    parser.add_argument("--max-len", type=int, default=512, help="Reranker max pair length.")
    parser.add_argument("--pad-to-multiple-of", type=int, default=8)
    parser.add_argument("--train-group-size", type=int, default=8)
    parser.add_argument("--max-example-num-per-dataset", type=int)
    parser.add_argument("--small-threshold", type=int)
    parser.add_argument("--drop-threshold", type=int)
    add_bool_arg(parser, "--knowledge-distillation", default=False)
    add_bool_arg(parser, "--same-dataset-within-batch", default=None)
    add_bool_arg(parser, "--overwrite-output-dir", default=True)
    add_bool_arg(parser, "--gradient-checkpointing", default=True)
    parser.add_argument("--query-instruction-for-retrieval")
    parser.add_argument("--passage-instruction-for-retrieval")
    parser.add_argument("--query-instruction-for-rerank")
    parser.add_argument("--passage-instruction-for-rerank")
    parser.add_argument("--query-instruction-format", default="{}{}")
    parser.add_argument("--passage-instruction-format", default="{}{}")
    parser.add_argument("--sentence-pooling-method", choices=("cls", "mean", "last_token"))
    add_bool_arg(parser, "--normalize-embeddings", default=True)
    add_bool_arg(parser, "--negatives-cross-device", default=None)
    parser.add_argument("--temperature", type=float, default=0.02)
    parser.add_argument("--sub-batch-size", type=int)
    parser.add_argument("--kd-loss-type", choices=("kl_div", "m3_kd_loss"))
    add_bool_arg(parser, "--use-lora", default=None)
    parser.add_argument("--lora-rank", type=int, default=32)
    parser.add_argument("--lora-alpha", type=float, default=64)
    parser.add_argument("--lora-dropout", type=float)
    parser.add_argument("--target-modules", nargs="+")
    parser.add_argument("--additional-special-tokens", nargs="+")
    add_bool_arg(parser, "--save-merged-lora-model", default=True)
    add_bool_arg(parser, "--use-flash-attn", default=None)
    add_bool_arg(parser, "--trust-remote-code", default=None)
    add_bool_arg(parser, "--m3-unified", default=None)
    add_bool_arg(parser, "--m3-self-distill", default=None)
    add_bool_arg(parser, "--fix-encoder", default=None)
    parser.add_argument("--self-distill-start-step", type=int)
    add_bool_arg(parser, "--retrieval-use-examples", default=None)
    parser.add_argument("--example-query-max-len", type=int)
    parser.add_argument("--example-passage-max-len", type=int)
    parser.add_argument("--icl-suffix-str")
    parser.add_argument("--sep-token")
    parser.add_argument("--model-type")
    parser.add_argument("--start-layer", type=int)
    add_bool_arg(parser, "--head-multi", default=None)
    parser.add_argument("--head-type")
    parser.add_argument("--extra-arg", action="append", default=[], help="Extra raw argument, repeatable, e.g. --extra-arg='--token' --extra-arg='$HF_TOKEN'.")
    return parser.parse_args()


def add_pair(command: list[str], flag: str, value: object | None) -> None:
    if value is not None:
        command.extend([flag, str(value)])


def add_bool_pair(command: list[str], flag: str, value: bool | None) -> None:
    if value is not None:
        command.extend([flag, "True" if value else "False"])


def quote_command(command: list[str]) -> str:
    return " \\\n  ".join(shlex.quote(part) for part in command)


def warn(message: str, warnings: list[str]) -> None:
    warnings.append(message)


def main() -> int:
    args = parse_args()
    spec = FAMILIES[args.family]
    warnings: list[str] = []

    model_name = args.model_name_or_path or spec["default_model"]
    precision = args.precision or spec["precision"]
    pooling = args.sentence_pooling_method or spec.get("pooling")
    kd_loss = args.kd_loss_type or spec.get("kd_loss")

    if args.nproc_per_node < 1:
        print("error: --nproc-per-node must be >= 1", file=sys.stderr)
        return 2
    if precision == "bf16":
        warn("bf16 requires hardware and PyTorch support; use fp16 or none if unsupported.", warnings)
    if args.deepspeed and not Path(args.deepspeed).exists():
        warn(f"DeepSpeed config does not exist yet: {args.deepspeed}", warnings)
    if args.use_flash_attn:
        warn("use_flash_attn=True requires flash-attn and compatible CUDA; omit it if unavailable.", warnings)
    if args.use_lora and spec["kind"] == "embedder" and "decoder" not in args.family:
        warn("LoRA is typically used for decoder-only families; verify support for this family.", warnings)
    if args.family == "embedder-decoder-icl" and args.same_dataset_within_batch is not True:
        warn("ICL embedder examples use same_dataset_within_batch=True; verify before execution.", warnings)
    if args.knowledge_distillation:
        warn("knowledge_distillation=True requires aligned pos_scores and neg_scores in every record.", warnings)
    if args.negatives_cross_device:
        warn("negatives_cross_device increases distributed communication and memory pressure.", warnings)
    if args.overwrite_output_dir:
        warn("overwrite_output_dir=True can replace existing checkpoints; verify output_dir.", warnings)

    command = ["torchrun", "--nproc_per_node", str(args.nproc_per_node), "-m", spec["module"]]
    add_pair(command, "--model_name_or_path", model_name)
    add_pair(command, "--cache_dir", args.cache_dir)
    add_bool_pair(command, "--trust_remote_code", args.trust_remote_code)

    if spec["kind"] == "reranker":
        add_pair(command, "--model_type", args.model_type or ("decoder" if "decoder" in args.family else None))

    if "decoder" in args.family:
        add_bool_pair(command, "--use_lora", args.use_lora if args.use_lora is not None else True)
        add_pair(command, "--lora_rank", args.lora_rank)
        add_pair(command, "--lora_alpha", args.lora_alpha)
        add_pair(command, "--lora_dropout", args.lora_dropout)
        if args.target_modules:
            command.append("--target_modules")
            command.extend(args.target_modules)
        add_bool_pair(command, "--use_flash_attn", args.use_flash_attn)
        if args.additional_special_tokens:
            command.append("--additional_special_tokens")
            command.extend(args.additional_special_tokens)
        add_bool_pair(command, "--save_merged_lora_model", args.save_merged_lora_model)

    if args.family == "reranker-decoder-layerwise":
        add_pair(command, "--start_layer", args.start_layer if args.start_layer is not None else 8)
        add_bool_pair(command, "--head_multi", args.head_multi if args.head_multi is not None else True)
        add_pair(command, "--head_type", args.head_type or "simple")

    command.append("--train_data")
    command.extend(args.train_data)
    add_pair(command, "--cache_path", args.cache_path)
    add_pair(command, "--train_group_size", args.train_group_size)
    add_pair(command, "--query_max_len", args.query_max_len)
    add_pair(command, "--passage_max_len", args.passage_max_len)
    if spec["kind"] == "reranker":
        add_pair(command, "--max_len", args.max_len)
    add_pair(command, "--pad_to_multiple_of", args.pad_to_multiple_of)
    add_pair(command, "--max_example_num_per_dataset", args.max_example_num_per_dataset)
    add_bool_pair(command, "--knowledge_distillation", args.knowledge_distillation)
    add_bool_pair(command, "--same_dataset_within_batch", args.same_dataset_within_batch)
    add_pair(command, "--small_threshold", args.small_threshold)
    add_pair(command, "--drop_threshold", args.drop_threshold)

    if spec["kind"] == "embedder":
        add_pair(command, "--query_instruction_for_retrieval", args.query_instruction_for_retrieval)
        add_pair(command, "--passage_instruction_for_retrieval", args.passage_instruction_for_retrieval)
    else:
        add_pair(command, "--query_instruction_for_rerank", args.query_instruction_for_rerank)
        add_pair(command, "--passage_instruction_for_rerank", args.passage_instruction_for_rerank)
        add_pair(command, "--sep_token", args.sep_token)
    add_pair(command, "--query_instruction_format", args.query_instruction_format)
    add_pair(command, "--passage_instruction_format", args.passage_instruction_format)

    if args.family == "embedder-decoder-icl":
        add_pair(command, "--example_query_max_len", args.example_query_max_len if args.example_query_max_len is not None else 256)
        add_pair(command, "--example_passage_max_len", args.example_passage_max_len if args.example_passage_max_len is not None else 256)
        add_bool_pair(command, "--retrieval_use_examples", args.retrieval_use_examples if args.retrieval_use_examples is not None else True)
        add_pair(command, "--icl_suffix_str", args.icl_suffix_str or "\n<response>")

    add_pair(command, "--output_dir", args.output_dir)
    add_bool_pair(command, "--overwrite_output_dir", args.overwrite_output_dir)
    add_pair(command, "--learning_rate", args.learning_rate or ("6e-5" if args.family == "reranker-encoder-base" else "2e-4" if "decoder" in args.family and spec["kind"] == "reranker" else "1e-5"))
    if precision != "none":
        command.append(f"--{precision}")
    add_pair(command, "--num_train_epochs", args.num_train_epochs)
    add_pair(command, "--per_device_train_batch_size", args.per_device_train_batch_size)
    add_pair(command, "--gradient_accumulation_steps", args.gradient_accumulation_steps)
    add_bool_pair(command, "--dataloader_drop_last", True)
    add_pair(command, "--warmup_ratio", args.warmup_ratio)
    add_bool_pair(command, "--gradient_checkpointing", args.gradient_checkpointing)
    add_pair(command, "--weight_decay", args.weight_decay)
    add_pair(command, "--deepspeed", args.deepspeed)
    add_pair(command, "--logging_steps", args.logging_steps)
    add_pair(command, "--save_steps", args.save_steps)
    add_pair(command, "--max_steps", args.max_steps)

    if spec["kind"] == "embedder":
        add_bool_pair(command, "--negatives_cross_device", args.negatives_cross_device if args.negatives_cross_device is not None else True)
        add_pair(command, "--temperature", args.temperature)
        add_pair(command, "--sentence_pooling_method", pooling)
        add_bool_pair(command, "--normalize_embeddings", args.normalize_embeddings)
        add_pair(command, "--sub_batch_size", args.sub_batch_size)
        add_pair(command, "--kd_loss_type", kd_loss)
        if args.family == "embedder-m3":
            add_bool_pair(command, "--unified_finetuning", args.m3_unified if args.m3_unified is not None else True)
            add_bool_pair(command, "--use_self_distill", args.m3_self_distill if args.m3_self_distill is not None else True)
            add_bool_pair(command, "--fix_encoder", args.fix_encoder if args.fix_encoder is not None else False)
            add_pair(command, "--self_distill_start_step", args.self_distill_start_step if args.self_distill_start_step is not None else 0)

    command.extend(args.extra_arg)

    if warnings:
        print("# Warnings", file=sys.stderr)
        for item in warnings:
            print(f"# - {item}", file=sys.stderr)
    print(quote_command(command))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
