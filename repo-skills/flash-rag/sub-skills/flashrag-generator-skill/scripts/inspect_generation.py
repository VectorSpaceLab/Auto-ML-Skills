#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.output.read_text(encoding="utf-8"))
    print("has_prompt: " + str("prompt" in payload).lower())
    print("pred: " + str(payload.get("pred", ""))[:200])
    ok = bool(payload.get("pred"))
    print(f"valid: {str(ok).lower()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
