#!/usr/bin/env python3
"""Create a vLLM embedding request payload."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="BAAI/bge-small-en-v1.5")
    parser.add_argument("--input", action="append", default=["hello", "world"])
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    payload = {"model": args.model, "input": args.input}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
