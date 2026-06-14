#!/usr/bin/env python3
"""Check LangSmith import and evaluation-related env vars without network calls."""

from __future__ import annotations

import argparse
import importlib.metadata as metadata
import json
import os


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-key", action="store_true")
    args = parser.parse_args()
    try:
        version = metadata.version("langsmith")
        importable = True
    except Exception as exc:
        version = None
        importable = False
        error = f"{type(exc).__name__}: {exc}"
    else:
        error = None
    env = {name: bool(os.environ.get(name)) for name in ["LANGSMITH_API_KEY", "LANGSMITH_TRACING", "LANGSMITH_PROJECT", "LANGSMITH_ENDPOINT"]}
    result = {"importable": importable, "version": version, "env_present": env}
    if error:
        result["error"] = error
    result["pass"] = importable and (env["LANGSMITH_API_KEY"] or not args.require_key)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
