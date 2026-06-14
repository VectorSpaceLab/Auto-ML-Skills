#!/usr/bin/env python3
"""Scan Python files for common LangChain classic/legacy imports."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PATTERNS = {
    "classic_package": re.compile(r"langchain_classic"),
    "legacy_chains": re.compile(r"from\s+langchain\.chains|import\s+langchain\.chains"),
    "legacy_memory": re.compile(r"from\s+langchain\.memory|import\s+langchain\.memory"),
    "legacy_models": re.compile(r"from\s+langchain\.(llms|chat_models|embeddings)"),
    "legacy_loaders": re.compile(r"from\s+langchain\.document_loaders|from\s+langchain\.text_splitter"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    findings = []
    for raw in args.paths:
        path = Path(raw)
        files = [path] if path.is_file() else sorted(path.rglob("*.py"))
        for file in files:
            text = file.read_text(encoding="utf-8", errors="replace")
            for name, pattern in PATTERNS.items():
                if pattern.search(text):
                    findings.append({"file": str(file), "pattern": name})
    print(json.dumps({"findings": findings, "count": len(findings)}, indent=2, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
