#!/usr/bin/env python3
"""No-key smoke test for LangChain text splitting."""

from __future__ import annotations

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunk-size", type=int, default=40)
    parser.add_argument("--chunk-overlap", type=int, default=8)
    args = parser.parse_args()

    from langchain_core.documents import Document
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    text = "Alpha beta gamma. " * 12
    splitter = RecursiveCharacterTextSplitter(chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap)
    chunks = splitter.split_text(text)
    docs = splitter.split_documents([Document(page_content=text, metadata={"source": "demo"})])
    result = {
        "string_chunks": len(chunks),
        "document_chunks": len(docs),
        "max_chunk_len": max(map(len, chunks)) if chunks else 0,
        "metadata_preserved": all(d.metadata.get("source") == "demo" for d in docs),
    }
    result["pass"] = result["string_chunks"] > 1 and result["metadata_preserved"] and result["max_chunk_len"] <= args.chunk_size
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
