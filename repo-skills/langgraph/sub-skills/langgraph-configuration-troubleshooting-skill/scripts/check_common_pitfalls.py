#!/usr/bin/env python3
"""Static checks for common LangGraph pitfalls."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CHECKS = [
    ("deprecated_message_graph", re.compile(r"\bMessageGraph\s*\("), "Prefer StateGraph with add_messages/MessagesState."),
    ("deprecated_config_schema", re.compile(r"\bconfig_schema\s*="), "Prefer context_schema."),
    ("interrupt_import", re.compile(r"\binterrupt\s*\("), "Interrupt workflows need a checkpointer and thread_id."),
    ("compile_checkpointer", re.compile(r"\.compile\s*\([^)]*checkpointer\s*="), "Checkpointed graphs need configurable.thread_id at runtime."),
    ("conditional_edges", re.compile(r"\.add_conditional_edges\s*\("), "Use path_map or Literal return types for clear routing."),
]


def check_file(path: Path) -> list[dict[str, str | int]]:
    text = path.read_text(encoding="utf-8")
    findings = []
    if path.name == "langgraph.json":
        try:
            data = json.loads(text)
            if not data.get("graphs"):
                findings.append({"file": str(path), "line": 1, "check": "graphs", "message": "Missing graphs object."})
            if not data.get("dependencies"):
                findings.append({"file": str(path), "line": 1, "check": "dependencies", "message": "Missing dependencies list."})
        except json.JSONDecodeError as exc:
            findings.append({"file": str(path), "line": exc.lineno, "check": "json", "message": exc.msg})
        return findings
    for check, pattern, message in CHECKS:
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            findings.append({"file": str(path), "line": line, "check": check, "message": message})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    findings = []
    for path in args.paths:
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.suffix == ".py" or child.name == "langgraph.json":
                    findings.extend(check_file(child))
        elif path.suffix == ".py" or path.name == "langgraph.json":
            findings.extend(check_file(path))
    print(json.dumps({"valid": True, "findings": findings}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
