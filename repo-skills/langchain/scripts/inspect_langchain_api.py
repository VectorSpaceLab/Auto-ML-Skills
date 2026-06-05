#!/usr/bin/env python3
"""Read-only import and signature inspection for LangChain public APIs."""

from __future__ import annotations

import argparse
import importlib
import inspect
import json


DEFAULT_OBJECTS = [
    "langchain_core.prompts.ChatPromptTemplate",
    "langchain_core.prompts.PromptTemplate",
    "langchain_core.runnables.RunnableLambda",
    "langchain_core.runnables.RunnablePassthrough",
    "langchain_core.output_parsers.StrOutputParser",
    "langchain_core.output_parsers.JsonOutputParser",
    "langchain_core.tools.tool",
    "langchain_core.embeddings.DeterministicFakeEmbedding",
    "langchain_core.vectorstores.InMemoryVectorStore",
]


def inspect_object(path: str) -> dict[str, object]:
    module_name, _, attr_name = path.rpartition(".")
    row: dict[str, object] = {"path": path, "ok": False}
    try:
        module = importlib.import_module(module_name)
        obj = getattr(module, attr_name)
        row["ok"] = True
        row["type"] = type(obj).__name__
        try:
            row["signature"] = str(inspect.signature(obj))
        except Exception as exc:
            row["signature_error"] = f"{type(exc).__name__}: {exc}"
        row["doc_present"] = bool(inspect.getdoc(obj))
    except Exception as exc:
        row["error"] = f"{type(exc).__name__}: {exc}"
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("objects", nargs="*", help="Fully qualified objects to inspect.")
    args = parser.parse_args()
    objects = args.objects or DEFAULT_OBJECTS
    results = [inspect_object(path) for path in objects]
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0 if all(row["ok"] for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
