#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import read_simple_yaml


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--split", default="test")
    parser.add_argument("--gpu-id", default="0")
    args = parser.parse_args()
    cfg = read_simple_yaml(args.config)
    cmd = [
        "python",
        "<vendored-methods-runner>/run_exp.py",
        "--method_name",
        str(cfg["method_name"]),
        "--split",
        args.split,
        "--dataset_name",
        str(cfg["dataset_name"]),
        "--gpu_id",
        args.gpu_id,
    ]
    payload = {
        "config": str(args.config),
        "command": cmd,
        "note": "FlashRAG named methods are demonstrated by a public repo example script, not a stable installed-package CLI. Vendor/adapt that runner before executing this command.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    print(" ".join(cmd))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
