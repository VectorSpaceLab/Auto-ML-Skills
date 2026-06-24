#!/usr/bin/env python3
"""No-key smoke test for LangChain document loading."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", default="LangChain loader smoke test.")
    args = parser.parse_args()

    from langchain_community.document_loaders import TextLoader

    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "sample.txt"
        path.write_text(args.text, encoding="utf-8")
        docs = TextLoader(str(path), encoding="utf-8").load()

    result = {
        "documents": len(docs),
        "content": docs[0].page_content if docs else "",
        "metadata_keys": sorted(docs[0].metadata.keys()) if docs else [],
    }
    result["pass"] = len(docs) == 1 and args.text in result["content"] and "source" in result["metadata_keys"]
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
