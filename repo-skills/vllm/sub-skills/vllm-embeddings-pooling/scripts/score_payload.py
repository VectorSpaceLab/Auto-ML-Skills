#!/usr/bin/env python3
"""Create a candidate vLLM score/rerank request payload."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="cross-encoder/ms-marco-MiniLM-L-6-v2")
    parser.add_argument("--text-1", default="what is vLLM?")
    parser.add_argument("--text-2", default="vLLM is an inference and serving engine for LLMs.")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    payload = {"model": args.model, "text_1": args.text_1, "text_2": args.text_2}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
