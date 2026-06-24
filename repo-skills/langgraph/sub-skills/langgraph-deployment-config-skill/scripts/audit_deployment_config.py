#!/usr/bin/env python3
"""Static audit for LangGraph deployment configuration JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

SECRET_WORDS = ["api_key", "apikey", "secret", "token", "password"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args()
    path = Path(args.path)
    data = json.loads(path.read_text(encoding="utf-8"))
    findings = []
    if "graphs" not in data or not isinstance(data["graphs"], dict) or not data["graphs"]:
        findings.append("missing non-empty graphs mapping")
    if "dependencies" not in data:
        findings.append("missing dependencies")
    if "python_version" not in data:
        findings.append("missing python_version")
    raw = json.dumps(data).lower()
    for word in SECRET_WORDS:
        if word in raw:
            findings.append(f"possible secret-like key in config: {word}")
    for name, spec in data.get("graphs", {}).items():
        if not isinstance(spec, str) or ":" not in spec:
            findings.append(f"graph {name!r} should be an import spec containing ':'")
    print(json.dumps({"valid": not findings, "findings": findings}, indent=2, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
