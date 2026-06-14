#!/usr/bin/env python3
"""Inspect advanced LangChain retriever imports without running external services."""

from __future__ import annotations

import importlib
import inspect
import json


TARGETS = [
    "langchain_classic.retrievers.MultiQueryRetriever",
    "langchain_classic.retrievers.ContextualCompressionRetriever",
    "langchain_classic.retrievers.EnsembleRetriever",
    "langchain_classic.retrievers.MultiVectorRetriever",
    "langchain_classic.retrievers.ParentDocumentRetriever",
    "langchain_classic.retrievers.SelfQueryRetriever",
    "langchain_classic.retrievers.TimeWeightedVectorStoreRetriever",
    "langchain_community.retrievers.BM25Retriever",
]


def inspect_target(target: str) -> dict[str, object]:
    modname, attr = target.rsplit(".", 1)
    try:
        obj = getattr(importlib.import_module(modname), attr)
        return {"target": target, "ok": True, "signature": str(inspect.signature(obj))}
    except Exception as exc:  # noqa: BLE001 - diagnostic script
        return {"target": target, "ok": False, "error": f"{type(exc).__name__}: {exc}"}


def main() -> int:
    rows = [inspect_target(target) for target in TARGETS]
    result = {"targets": rows, "pass": all(row["ok"] for row in rows if "BM25" not in row["target"])}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
