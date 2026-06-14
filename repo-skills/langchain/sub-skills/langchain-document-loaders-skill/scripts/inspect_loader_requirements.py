#!/usr/bin/env python3
"""Check common LangChain loader-related imports without network calls."""

from __future__ import annotations

import argparse
import importlib
import json

DEFAULTS = {
    "text-loader": "langchain_community.document_loaders",
    "core-documents": "langchain_core.documents",
    "text-splitters": "langchain_text_splitters",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("modules", nargs="*", help="Additional module names to import-check.")
    args = parser.parse_args()
    checks = dict(DEFAULTS)
    for module in args.modules:
        checks[module] = module
    out = []
    for name, module in checks.items():
        try:
            importlib.import_module(module)
            out.append({"name": name, "module": module, "importable": True})
        except Exception as exc:
            out.append({"name": name, "module": module, "importable": False, "error": f"{type(exc).__name__}: {exc}"})
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if all(item["importable"] for item in out if item["name"] in DEFAULTS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
