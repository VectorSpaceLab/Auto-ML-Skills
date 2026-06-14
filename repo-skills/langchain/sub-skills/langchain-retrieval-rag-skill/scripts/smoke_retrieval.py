#!/usr/bin/env python3
"""No-key smoke test for LangChain retrieval and text splitting."""

from __future__ import annotations

import json


def main() -> int:
    from langchain_core.documents import Document
    from langchain_core.embeddings import DeterministicFakeEmbedding
    from langchain_core.vectorstores import InMemoryVectorStore
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    docs = [
        Document(page_content="LangChain composes runnables with LCEL.", metadata={"id": "lcel"}),
        Document(page_content="Retrievers return relevant documents.", metadata={"id": "retrieval"}),
    ]
    splitter = RecursiveCharacterTextSplitter(chunk_size=40, chunk_overlap=5)
    chunks = splitter.split_documents(docs)
    store = InMemoryVectorStore(embedding=DeterministicFakeEmbedding(size=12))
    store.add_documents(chunks)
    hits = store.similarity_search("runnables", k=2)
    retriever_hits = store.as_retriever(search_kwargs={"k": 1}).invoke("documents")
    result = {
        "chunks": len(chunks),
        "hits": len(hits),
        "retriever_hits": len(retriever_hits),
        "metadata_present": bool(hits and "id" in hits[0].metadata),
    }
    result["pass"] = result["chunks"] >= 2 and result["hits"] == 2 and result["retriever_hits"] == 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
