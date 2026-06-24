#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect a Hugging Face dataset saved by LLaMA-Factory tokenized_path.")
    parser.add_argument("--tokenized-path", type=Path, required=True)
    parser.add_argument("--expect-split", default="train")
    args = parser.parse_args()

    path = args.tokenized_path
    print(f"tokenized_path: {path.resolve()}")
    if not path.is_dir():
        print("valid: false")
        print("- tokenized path does not exist")
        return 1
    try:
        from datasets import load_from_disk
    except Exception as exc:
        print("valid: false")
        print(f"- cannot import datasets: {type(exc).__name__}: {exc}")
        return 1

    ds = load_from_disk(str(path))
    splits = list(ds.keys()) if hasattr(ds, "keys") else ["train"]
    print("splits: " + ",".join(splits))
    if args.expect_split not in splits:
        print("valid: false")
        print(f"- expected split {args.expect_split!r} not found")
        return 1
    split = ds[args.expect_split] if hasattr(ds, "keys") else ds
    print(f"{args.expect_split}_rows: {len(split)}")
    if len(split) == 0:
        print("valid: false")
        print("- split is empty")
        return 1
    print("features: " + ",".join(split.features.keys()))
    sample = split[0]
    for key, value in sample.items():
        if isinstance(value, list):
            print(f"{key}_len: {len(value)}")
        else:
            print(f"{key}: {value}")
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
