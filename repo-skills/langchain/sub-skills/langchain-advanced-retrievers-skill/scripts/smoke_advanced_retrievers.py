#!/usr/bin/env python3
"""No-key smoke for ParentDocumentRetriever and EnsembleRetriever."""

from __future__ import annotations

import json


def main() -> int:
    from langchain_classic.retrievers import EnsembleRetriever, ParentDocumentRetriever
    from langchain_classic.storage import create_kv_docstore
    from langchain_core.documents import Document
    from langchain_core.embeddings import DeterministicFakeEmbedding
    from langchain_core.stores import InMemoryByteStore
    from langchain_core.vectorstores import InMemoryVectorStore
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    embedding = DeterministicFakeEmbedding(size=12)
    parent_store = InMemoryVectorStore(embedding=embedding)
    docstore = create_kv_docstore(InMemoryByteStore())
    parent_retriever = ParentDocumentRetriever(
        vectorstore=parent_store,
        docstore=docstore,
        child_splitter=RecursiveCharacterTextSplitter(chunk_size=40, chunk_overlap=0),
    )
    parent_docs = [
        Document(
            page_content="LangChain parent retrievers embed child chunks but return full parent documents.",
            metadata={"source_id": "parent-1"},
        )
    ]
    parent_retriever.add_documents(parent_docs)
    parent_hits = parent_retriever.invoke("child chunks")

    lexical_like_store = InMemoryVectorStore(embedding=embedding)
    lexical_like_store.add_documents(
        [Document(page_content="Lexical retrievers and vector retrievers can be ensembled.", metadata={"source_id": "lex-1"})]
    )
    ensemble = EnsembleRetriever(
        retrievers=[
            parent_store.as_retriever(search_kwargs={"k": 1}),
            lexical_like_store.as_retriever(search_kwargs={"k": 1}),
        ],
        weights=[0.5, 0.5],
        id_key="source_id",
    )
    ensemble_hits = ensemble.invoke("retrievers")

    result = {
        "parent_hits": len(parent_hits),
        "parent_returned_full_doc": bool(parent_hits and "full parent" in parent_hits[0].page_content),
        "ensemble_hits": len(ensemble_hits),
        "ensemble_sources": [doc.metadata.get("source_id") for doc in ensemble_hits],
    }
    result["pass"] = (
        result["parent_hits"] == 1
        and result["parent_returned_full_doc"]
        and result["ensemble_hits"] >= 2
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
