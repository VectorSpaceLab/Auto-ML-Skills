#!/usr/bin/env python3
"""Run bundled no-key LangChain smoke scripts."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def discover_smokes() -> list[str]:
    scripts = []
    for path in sorted((ROOT / "sub-skills").glob("*/scripts/smoke_*.py")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.endswith("smoke_local_hf_model.py"):
            continue
        scripts.append(rel)
    return scripts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print JSON summary only.")
    args = parser.parse_args()

    results = []
    for rel in discover_smokes():
        path = ROOT / rel
        proc = subprocess.run(
            [sys.executable, str(path)],
            cwd=path.parent,
            text=True,
            capture_output=True,
            check=False,
        )
        results.append(
            {
                "script": rel,
                "returncode": proc.returncode,
                "pass": proc.returncode == 0,
                "stdout": proc.stdout.strip(),
                "stderr": proc.stderr.strip(),
            }
        )
    if args.json:
        print(json.dumps(results, indent=2, sort_keys=True))
    else:
        for row in results:
            status = "PASS" if row["pass"] else "FAIL"
            print(f"{status} {row['script']}")
            if row["stdout"]:
                print(row["stdout"])
            if row["stderr"]:
                print(row["stderr"])
    return 0 if all(row["pass"] for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
