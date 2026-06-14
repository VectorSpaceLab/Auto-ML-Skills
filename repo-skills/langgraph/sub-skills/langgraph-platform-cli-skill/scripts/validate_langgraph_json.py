#!/usr/bin/env python3
"""Validate a langgraph.json file without starting a server."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SPEC_RE = re.compile(r"^[A-Za-z0-9_./:-]+:[A-Za-z_][A-Za-z0-9_]*$")


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return ["root must be a JSON object"]
    deps = data.get("dependencies")
    graphs = data.get("graphs")
    if not isinstance(deps, list) or not deps:
        errors.append("dependencies must be a non-empty list")
    elif not all(isinstance(x, str) and x for x in deps):
        errors.append("dependencies entries must be non-empty strings")
    if not isinstance(graphs, dict) or not graphs:
        errors.append("graphs must be a non-empty object")
    else:
        for name, spec in graphs.items():
            if not isinstance(name, str) or not name:
                errors.append("graph names must be non-empty strings")
            if not isinstance(spec, str) or not SPEC_RE.match(spec):
                errors.append(f"graph {name!r} spec should look like module_or_path.py:graph")
    if "python_version" in data and str(data["python_version"]) not in {"3.10", "3.11", "3.12", "3.13"}:
        errors.append("python_version should be a supported Python version string")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate(args.path)
    if errors:
        print("\n".join(errors))
        return 1
    print({"valid": True, "path": str(args.path)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
