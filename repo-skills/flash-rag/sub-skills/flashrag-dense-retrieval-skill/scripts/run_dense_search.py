#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import env_for


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=None, help="Optional installed package root to add to PYTHONPATH.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.package_root is not None:
        sys.path.insert(0, str(args.package_root.resolve()))
    from flashrag.config import Config
    from flashrag.utils import get_retriever

    config = Config(str(args.config))
    retriever = get_retriever(config)
    docs = retriever.search(args.query, num=config["retrieval_topk"])
    payload = {"query": args.query, "docs": docs}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"docs": len(docs), "output": str(args.output)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
