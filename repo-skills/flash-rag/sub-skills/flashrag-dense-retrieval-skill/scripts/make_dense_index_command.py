#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--retrieval-method", required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--save-dir", type=Path, required=True)
    parser.add_argument("--pooling-method", default="mean")
    parser.add_argument("--max-length", type=int, default=512)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--faiss-type", default="Flat")
    parser.add_argument("--use-fp16", action="store_true")
    parser.add_argument("--faiss-gpu", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cmd = [
        "python", "-m", "flashrag.retriever.index_builder",
        "--retrieval_method", args.retrieval_method,
        "--model_path", args.model_path,
        "--corpus_path", str(args.corpus),
        "--save_dir", str(args.save_dir),
        "--max_length", str(args.max_length),
        "--batch_size", str(args.batch_size),
        "--pooling_method", args.pooling_method,
        "--faiss_type", args.faiss_type,
    ]
    if args.use_fp16:
        cmd.append("--use_fp16")
    if args.faiss_gpu:
        cmd.append("--faiss_gpu")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("#!/usr/bin/env bash\nset -euo pipefail\n{}\n".format(" ".join(cmd)), encoding="utf-8")
    args.output.chmod(0o755)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
