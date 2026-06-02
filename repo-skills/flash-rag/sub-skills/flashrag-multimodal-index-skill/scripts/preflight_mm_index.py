#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.command.read_text(encoding="utf-8"))
    errors: list[str] = []
    corpus = Path(payload["corpus"])
    if not corpus.is_file():
        errors.append(f"corpus file missing: {corpus}")
    method = payload["retrieval_method"]
    if method != "bm25" and not payload.get("model_path"):
        print(f"warning: {method} real index build normally needs a CLIP model path")
    elif payload.get("model_path") and not Path(payload["model_path"]).exists():
        print(f"warning: model_path does not exist locally yet: {payload['model_path']}")
    print(f"retrieval_method: {method}")
    print(f"index_dir: {payload['index_dir']}")
    print("command: " + " ".join(payload["command"]))
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
