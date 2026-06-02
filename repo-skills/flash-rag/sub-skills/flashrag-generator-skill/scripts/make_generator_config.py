#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import write_yaml


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--framework", choices=["hf", "vllm", "fschat", "openai"], default="hf")
    parser.add_argument("--generator-model", required=True)
    parser.add_argument("--generator-model-path", default=None)
    parser.add_argument("--max-input-len", type=int, default=2048)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--max-tokens", type=int, default=64)
    args = parser.parse_args()
    cfg = {
        "framework": args.framework,
        "generator_model": args.generator_model,
        "generator_model_path": args.generator_model_path,
        "generator_max_input_len": args.max_input_len,
        "generator_batch_size": args.batch_size,
        "generation_params": {"do_sample": False, "max_tokens": args.max_tokens},
        "data_dir": "dataset",
        "save_dir": "outputs",
        "dataset_name": "nq",
        "split": ["test"],
        "metrics": ["em", "f1", "acc"],
    }
    write_yaml(args.output, cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
