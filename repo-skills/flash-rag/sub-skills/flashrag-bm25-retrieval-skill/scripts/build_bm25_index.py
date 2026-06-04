#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from flashrag_import_stubs import install_optional_import_stubs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=None, help="Optional installed package root to add to PYTHONPATH.")
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--save-dir", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    if args.package_root is not None:
        sys.path.insert(0, str(args.package_root.resolve()))
    corpus = args.corpus.resolve()
    save_dir = args.save_dir.resolve()
    index_dir = save_dir / "bm25"

    if not corpus.is_file():
        raise FileNotFoundError(corpus)
    if index_dir.exists():
        if args.overwrite:
            shutil.rmtree(index_dir)
        elif any(index_dir.iterdir()):
            raise FileExistsError(f"{index_dir} exists; pass --overwrite to rebuild")

    install_optional_import_stubs()
    from flashrag.retriever.index_builder import Index_Builder

    builder = Index_Builder(
        retrieval_method="bm25",
        model_path=None,
        corpus_path=str(corpus),
        save_dir=str(save_dir),
        max_length=180,
        batch_size=512,
        use_fp16=False,
        pooling_method="mean",
        bm25_backend="bm25s",
    )
    builder.build_index()

    payload = {"corpus": str(corpus), "save_dir": str(save_dir), "index_dir": str(index_dir)}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
