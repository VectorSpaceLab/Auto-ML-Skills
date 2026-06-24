#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--index-dir", required=True)
    parser.add_argument("--retrieval-method", choices=["openai-clip", "chinese-clip", "clip", "bm25"], default="openai-clip")
    parser.add_argument("--model-path", default=None)
    parser.add_argument("--batch-size", type=int, default=64)
    args = parser.parse_args()
    cmd = [
        "python",
        "-m",
        "flashrag.retriever.index_builder",
        "--retrieval_method",
        args.retrieval_method,
        "--corpus_path",
        args.corpus,
        "--save_dir",
        args.index_dir,
        "--batch_size",
        str(args.batch_size),
    ]
    if args.model_path:
        cmd.extend(["--model_path", args.model_path])
    payload = {
        "corpus": args.corpus,
        "index_dir": args.index_dir,
        "retrieval_method": args.retrieval_method,
        "model_path": args.model_path,
        "command": cmd,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    print(" ".join(cmd))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
