#!/usr/bin/env python3
"""Import-check common LangChain vector store integration packages."""

from __future__ import annotations

import argparse
import importlib
import json

DEFAULT_MODULES = ["langchain_core.vectorstores", "langchain_chroma", "langchain_qdrant"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("modules", nargs="*", default=DEFAULT_MODULES)
    args = parser.parse_args()
    out = []
    for module in args.modules:
        try:
            importlib.import_module(module)
            out.append({"module": module, "importable": True})
        except Exception as exc:
            out.append({"module": module, "importable": False, "error": f"{type(exc).__name__}: {exc}"})
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
