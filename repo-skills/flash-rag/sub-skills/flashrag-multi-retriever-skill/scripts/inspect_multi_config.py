#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()

    import yaml

    cfg = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    setting = cfg.get("multi_retriever_setting", {})
    retrievers = setting.get("retriever_list", [])
    print(f"use_multi_retriever: {cfg.get('use_multi_retriever')}")
    print(f"merge_method: {setting.get('merge_method')}")
    print(f"retrievers: {len(retrievers)}")
    for i, ret in enumerate(retrievers):
        print(f"retriever_{i}: {ret.get('retrieval_method')} topk={ret.get('retrieval_topk')} index={ret.get('index_path')}")
    ok = cfg.get("use_multi_retriever") is True and len(retrievers) >= 2
    print(f"valid: {str(ok).lower()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
