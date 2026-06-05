#!/usr/bin/env python3
"""No-key smoke for LangChain stores and document stores."""

from __future__ import annotations

import asyncio
import json


async def async_store_check(store) -> bool:  # noqa: ANN001 - generic store protocol
    await store.amset([("async", {"ok": True})])
    values = await store.amget(["async"])
    keys = [key async for key in store.ayield_keys()]
    return values == [{"ok": True}] and "async" in keys


def main() -> int:
    from langchain_classic.storage import create_kv_docstore
    from langchain_core.documents import Document
    from langchain_core.stores import InMemoryByteStore, InMemoryStore

    store = InMemoryStore()
    store.mset([("a", {"x": 1}), ("b", {"x": 2})])
    sync_values = store.mget(["a", "b"])
    sync_keys = list(store.yield_keys())
    async_ok = asyncio.run(async_store_check(store))

    byte_store = InMemoryByteStore()
    byte_store.mset([("raw", b"value")])
    raw_ok = byte_store.mget(["raw"]) == [b"value"]

    docstore = create_kv_docstore(InMemoryByteStore())
    doc = Document(page_content="Docstore keeps parent documents.", metadata={"source": "smoke"})
    docstore.mset([("doc-1", doc)])
    restored = docstore.mget(["doc-1"])[0]
    doc_ok = restored is not None and restored.page_content == doc.page_content and restored.metadata == doc.metadata

    result = {
        "sync_values": sync_values,
        "sync_keys": sync_keys,
        "async_ok": async_ok,
        "raw_ok": raw_ok,
        "doc_ok": doc_ok,
    }
    result["pass"] = sync_values == [{"x": 1}, {"x": 2}] and async_ok and raw_ok and doc_ok
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
