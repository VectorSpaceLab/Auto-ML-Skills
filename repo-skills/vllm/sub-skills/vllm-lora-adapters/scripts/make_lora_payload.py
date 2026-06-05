#!/usr/bin/env python3
"""Create an OpenAI chat payload targeting a LoRA served model name."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--adapter-name", required=True)
    parser.add_argument("--prompt", default="Say hello in one short sentence.")
    parser.add_argument("--out", required=True)
    parser.add_argument("--max-tokens", type=int, default=16)
    args = parser.parse_args()
    payload = {
        "model": args.adapter_name,
        "messages": [{"role": "user", "content": args.prompt}],
        "temperature": 0,
        "max_tokens": args.max_tokens,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
