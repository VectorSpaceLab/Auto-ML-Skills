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
    parser.add_argument("--save-dir", required=True)
    parser.add_argument("--generator-model", default="llama3-8B-instruct")
    parser.add_argument("--model-path", default=None)
    parser.add_argument("--framework", default="hf")
    parser.add_argument("--max-new-tokens", type=int, default=64)
    args = parser.parse_args()
    cfg = {
        "save_dir": args.save_dir,
        "save_note": "multiturn",
        "framework": args.framework,
        "generator_model": args.generator_model,
        "generator_model_path": args.model_path,
        "model2path": {args.generator_model: args.model_path} if args.model_path else {},
        "generation_params": {"max_tokens": args.max_new_tokens},
        "metrics": ["em", "f1", "acc"],
        "retrieval_method": None,
        "retrieval_topk": 0,
        "save_intermediate_data": True,
    }
    write_yaml(args.output, cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
