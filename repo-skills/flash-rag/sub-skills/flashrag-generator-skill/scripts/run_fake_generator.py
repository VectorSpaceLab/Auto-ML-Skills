#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    prompt = args.prompt.read_text(encoding="utf-8")
    match = re.search(r"Question:\s*(.*?)\nAnswer:", prompt, flags=re.DOTALL)
    question = match.group(1).strip() if match else ""
    pred = "offline fake answer" if not question else f"offline fake answer for: {question}"
    payload = {"prompt": prompt, "pred": pred}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"pred": pred, "output": str(args.output)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
