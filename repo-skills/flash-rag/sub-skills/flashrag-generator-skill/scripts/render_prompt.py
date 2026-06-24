#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    parser.add_argument("--reference", action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    refs = "\n".join(f"Doc {i+1}: {r}" for i, r in enumerate(args.reference))
    prompt = "Answer the question"
    if refs:
        prompt += " using the references.\n\n" + refs
    prompt += f"\n\nQuestion: {args.question}\nAnswer:"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(prompt, encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
