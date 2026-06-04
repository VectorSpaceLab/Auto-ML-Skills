#!/usr/bin/env python3
"""Split FlagEmbedding training JSONL by maximum token length.

Example:
    python scripts/split_data_by_length.py \
      --input_path train_data \
      --output_dir train_data_split \
      --model_name_or_path BAAI/bge-m3 \
      --length_list 0 500 1000 2000 3000 4000 5000 6000 7000
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from pathlib import Path

import datasets
from datasets import Features, Sequence, Value, load_dataset
from tqdm import tqdm
from transformers import AutoTokenizer


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--cache_dir", default=None)
    parser.add_argument("--log_name", default=".split_log")
    parser.add_argument("--length_list", type=int, default=[0, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000], nargs="+")
    parser.add_argument("--model_name_or_path", default="BAAI/bge-m3")
    parser.add_argument("--num_proc", type=int, default=16)
    parser.add_argument("--overwrite", action="store_true", default=False)
    return parser.parse_args()


class SplitByLengthHandler:
    def __init__(
        self,
        model_name_or_path: str,
        cache_dir: str | None = None,
        num_proc: int = 16,
        length_list: list[int] | None = None,
        overwrite: bool = False,
    ) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.cache_dir = cache_dir
        self.num_proc = num_proc
        self.length_ranges = self._get_length_ranges(length_list or [0, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000])
        self.overwrite = overwrite

    @staticmethod
    def _get_length_ranges(length_list: list[int]) -> list[tuple[int, int | float]]:
        values = sorted(length_list)
        ranges = []
        for idx, left in enumerate(values):
            right = math.inf if idx == len(values) - 1 else values[idx + 1]
            if not 0 <= left < right:
                raise ValueError("length_list must be sorted into increasing non-negative ranges")
            ranges.append((left, right))
        return ranges

    def _map_func(self, examples: dict) -> dict:
        result = {"idx": [], "max_length": []}
        for idx, query, pos, neg in zip(examples["idx"], examples["query"], examples["pos"], examples["neg"]):
            all_texts = [query] + list(pos) + list(neg)
            max_len = max(len(self.tokenizer(text)["input_ids"]) for text in all_texts)
            result["idx"].append(idx)
            result["max_length"].append(max_len)
        return result

    def _load_json_dataset(self, file_path: str):
        features = Features({"query": Value("string"), "pos": Sequence(Value("string")), "neg": Sequence(Value("string"))})
        kd_features = Features(
            {
                "query": Value("string"),
                "pos": Sequence(Value("string")),
                "neg": Sequence(Value("string")),
                "pos_scores": Sequence(Value("float")),
                "neg_scores": Sequence(Value("float")),
            }
        )
        try:
            return load_dataset("json", data_files=file_path, cache_dir=self.cache_dir, features=features)["train"]
        except Exception:
            return load_dataset("json", data_files=file_path, cache_dir=self.cache_dir, features=kd_features)["train"]

    def _process_file(self, file_path: Path, output_prefix: Path) -> dict:
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dataset = self._load_json_dataset(str(file_path))
        dataset_with_idx = datasets.Dataset.from_list([{**row, "idx": i} for i, row in enumerate(dataset)])
        mapped = dataset_with_idx.map(self._map_func, batched=True, num_proc=self.num_proc)

        split_info: dict[str, int] = {}
        for left, right in self.length_ranges:
            save_path = Path(f"{output_prefix}_len-{left}-{right}.jsonl")
            if save_path.exists() and not self.overwrite:
                print(f"{save_path} exists, skip")
                continue
            indices = mapped.filter(lambda row, l=left, r=right: l <= row["max_length"] < r, num_proc=self.num_proc)
            split_dataset = dataset_with_idx.select(indices["idx"]).remove_columns("idx")
            split_info[f"len-{left}-{right}"] = len(split_dataset)
            if len(split_dataset) > 0:
                split_dataset.to_json(str(save_path), force_ascii=False)

        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        size = len(dataset)
        return {
            "file_name": file_path.name,
            "size": size,
            "avg_length": sum(mapped["max_length"]) / size if size else 0,
            "file_path": str(file_path),
            "start_time": start_time,
            "end_time": end_time,
            "split_info": split_info,
        }

    def run(self, input_path: str, output_dir: str, log_name: str) -> None:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        input_obj = Path(input_path)
        files = sorted(input_obj.glob("*.jsonl")) if input_obj.is_dir() else [input_obj]
        log_infos = []
        for file_path in tqdm(files, desc="files"):
            if file_path.suffix != ".jsonl":
                continue
            output_prefix = out_dir / file_path.stem
            log_infos.append(self._process_file(file_path, output_prefix))
        with (out_dir / log_name).open("a", encoding="utf-8") as handle:
            for info in log_infos:
                handle.write(json.dumps(info, ensure_ascii=False) + "\n")


def main() -> None:
    args = get_args()
    handler = SplitByLengthHandler(
        model_name_or_path=args.model_name_or_path,
        cache_dir=args.cache_dir,
        num_proc=args.num_proc,
        length_list=args.length_list,
        overwrite=args.overwrite,
    )
    handler.run(args.input_path, args.output_dir, args.log_name)
    print("DONE")


if __name__ == "__main__":
    main()
