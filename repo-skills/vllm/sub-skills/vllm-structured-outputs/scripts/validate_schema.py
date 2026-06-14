#!/usr/bin/env python3
"""Validate JSON syntax and basic JSON Schema shape."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("schema")
    args = parser.parse_args()
    data = json.loads(Path(args.schema).read_text(encoding="utf-8"))
    issues = []
    if not isinstance(data, dict):
        issues.append("schema must be an object")
    if data.get("type") != "object":
        issues.append("smoke schemas should use type=object")
    if not isinstance(data.get("properties"), dict):
        issues.append("missing object properties")
    print(json.dumps({"valid": not issues, "issues": issues}, indent=2))
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
