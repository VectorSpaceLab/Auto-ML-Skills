#!/usr/bin/env python3
"""Create tiny self-contained LLaMA-Factory demo datasets.

Use this when a future agent needs a smoke-test dataset and should not depend on
demo files from a source checkout.

Example:
  python scripts/make_demo_data.py --task sft --dataset-dir ./data --dataset-name tiny_sft
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def write_json(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_dataset_info(dataset_dir: Path, name: str, filename: str, task: str) -> None:
    info_path = dataset_dir / "dataset_info.json"
    info: dict[str, Any] = {}
    if info_path.exists():
        info = json.loads(info_path.read_text(encoding="utf-8"))

    if task == "sft":
        entry: dict[str, Any] = {
            "file_name": filename,
            "columns": {"prompt": "instruction", "query": "input", "response": "output"},
        }
    elif task == "pt":
        entry = {
            "file_name": filename,
            "columns": {"prompt": "text"},
        }
    elif task == "dpo":
        entry = {
            "file_name": filename,
            "ranking": True,
            "formatting": "sharegpt",
            "columns": {"messages": "conversations", "chosen": "chosen", "rejected": "rejected"},
        }
    elif task == "rm":
        entry = {
            "file_name": filename,
            "formatting": "sharegpt",
            "columns": {"chosen": "chosen", "rejected": "rejected"},
        }
    elif task == "kto":
        entry = {
            "file_name": filename,
            "formatting": "sharegpt",
            "columns": {"messages": "messages", "kto_tag": "label"},
            "tags": {"role_tag": "role", "content_tag": "content", "user_tag": "user", "assistant_tag": "assistant"},
        }
    else:
        raise ValueError(task)

    info[name] = entry
    info_path.write_text(json.dumps(info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rows_for(task: str) -> list[dict[str, Any]]:
    if task == "sft":
        return [
            {"instruction": "Convert this sentence to lowercase.", "input": "HELLO WORLD", "output": "hello world"},
            {"instruction": "Answer with the capital of France.", "input": "", "output": "Paris"},
        ]
    if task == "pt":
        return [
            {"text": "Machine learning systems learn patterns from data."},
            {"text": "Retrieval augmented generation combines search with generation."},
        ]
    if task == "dpo":
        return [
            {
                "conversations": [
                    {"from": "human", "value": "Which answer is concise and correct for the capital of France?"}
                ],
                "chosen": {"from": "gpt", "value": "Paris."},
                "rejected": {"from": "gpt", "value": "The capital of France is Berlin."},
            },
            {
                "conversations": [{"from": "human", "value": "Give one safe shell command to list files."}],
                "chosen": {"from": "gpt", "value": "Use `ls` to list files in the current directory."},
                "rejected": {"from": "gpt", "value": "Delete the directory first, then inspect it."},
            },
        ]
    if task == "rm":
        return [
            {
                "chosen": [
                    {"role": "user", "content": "Which answer is concise and correct for the capital of France?"},
                    {"role": "assistant", "content": "Paris."},
                ],
                "rejected": [
                    {"role": "user", "content": "Which answer is concise and correct for the capital of France?"},
                    {"role": "assistant", "content": "The capital of France is Berlin."},
                ],
            },
            {
                "chosen": [
                    {"role": "user", "content": "Give one safe shell command to list files."},
                    {"role": "assistant", "content": "Use `ls` to list files in the current directory."},
                ],
                "rejected": [
                    {"role": "user", "content": "Give one safe shell command to list files."},
                    {"role": "assistant", "content": "Delete the directory first, then inspect it."},
                ],
            },
        ]
    if task == "kto":
        return [
            {
                "messages": [
                    {"role": "user", "content": "Name the capital of France."},
                    {"role": "assistant", "content": "Paris."},
                ],
                "label": True,
            },
            {
                "messages": [
                    {"role": "user", "content": "Name the capital of France."},
                    {"role": "assistant", "content": "Berlin."},
                ],
                "label": False,
            },
        ]
    raise ValueError(task)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["sft", "pt", "dpo", "rm", "kto"], required=True)
    parser.add_argument("--dataset-dir", type=Path, required=True)
    parser.add_argument("--dataset-name", required=True)
    args = parser.parse_args()

    filename = f"{args.dataset_name}.json"
    write_json(args.dataset_dir / filename, rows_for(args.task))
    update_dataset_info(args.dataset_dir, args.dataset_name, filename, args.task)
    print(f"dataset_dir: {args.dataset_dir.resolve()}")
    print(f"dataset_name: {args.dataset_name}")
    print(f"data_file: {args.dataset_dir / filename}")
    print(f"dataset_info: {args.dataset_dir / 'dataset_info.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
