#!/usr/bin/env python3
"""Scan a Python file for LangChain imports that need a security review."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PATTERNS = {
    "shell_tool": re.compile(r"ShellTool|ShellToolMiddleware|HostExecutionPolicy"),
    "python_tool": re.compile(r"PythonREPL|PythonAstREPL|PythonTool"),
    "requests_tool": re.compile(r"RequestsToolkit|APIChain|allow_dangerous_requests"),
    "sql_tool": re.compile(r"SQLDatabaseToolkit|create_sql_agent|SQLDatabase"),
    "unsafe_store": re.compile(r"create_lc_store|pickle|deserialize"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    args = parser.parse_args()

    text = args.file.read_text(encoding="utf-8")
    findings = {
        name: [match.group(0) for match in pattern.finditer(text)]
        for name, pattern in PATTERNS.items()
    }
    findings = {name: hits for name, hits in findings.items() if hits}
    result = {"file": str(args.file), "findings": findings, "requires_review": bool(findings)}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
