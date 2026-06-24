#!/usr/bin/env python3
"""No-key smoke test for LangChain models and embeddings."""

from __future__ import annotations

import argparse
import importlib
import json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider-module", help="Optional provider module import to check.")
    args = parser.parse_args()

    from langchain_core.embeddings import DeterministicFakeEmbedding
    from langchain_core.language_models import FakeListChatModel, FakeListLLM

    chat = FakeListChatModel(responses=["chat-ok"])
    llm = FakeListLLM(responses=["llm-ok"])
    embed = DeterministicFakeEmbedding(size=8)
    chat_result = chat.invoke("hello").content
    llm_result = llm.invoke("hello")
    vector = embed.embed_query("hello")
    docs = embed.embed_documents(["a", "b"])

    result = {
        "chat": chat_result,
        "llm": llm_result,
        "embedding_dim": len(vector),
        "documents": len(docs),
        "pass": chat_result == "chat-ok" and llm_result == "llm-ok" and len(vector) == 8,
    }
    if args.provider_module:
        try:
            importlib.import_module(args.provider_module)
            result["provider_import"] = "ok"
        except Exception as exc:
            result["provider_import"] = f"{type(exc).__name__}: {exc}"
            result["pass"] = False
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
