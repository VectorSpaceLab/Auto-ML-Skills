#!/usr/bin/env python3
"""No-key smoke test for LangChain vectorstores and retrievers."""

from __future__ import annotations

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--k", type=int, default=2)
    args = parser.parse_args()

    from langchain_core.documents import Document
    from langchain_core.embeddings import DeterministicFakeEmbedding
    from langchain_core.vectorstores import InMemoryVectorStore

    docs = [
        Document(page_content="LCEL composes runnables.", metadata={"id": "lcel"}),
        Document(page_content="Vector stores retrieve embedded chunks.", metadata={"id": "vector"}),
        Document(page_content="Agents call tools.", metadata={"id": "agent"}),
    ]
    store = InMemoryVectorStore(embedding=DeterministicFakeEmbedding(size=16))
    ids = store.add_documents(docs, ids=[d.metadata["id"] for d in docs])
    hits = store.similarity_search("embedded chunks", k=args.k)
    retriever_hits = store.as_retriever(search_kwargs={"k": 1}).invoke("runnables")
    result = {
        "ids": ids,
        "hits": len(hits),
        "retriever_hits": len(retriever_hits),
        "metadata_ids": [d.metadata.get("id") for d in hits],
    }
    result["pass"] = len(ids) == 3 and result["hits"] == args.k and result["retriever_hits"] == 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
