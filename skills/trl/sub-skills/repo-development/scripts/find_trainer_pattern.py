#!/usr/bin/env python
"""Find a text pattern across TRL trainer source files.

Run from a TRL checkout. This is a lightweight helper for duplicated trainer
logic checks.

Example:
    python scripts/find_trainer_pattern.py "_generate_single_turn"
"""

from __future__ import annotations

import argparse
from pathlib import Path


ROOTS = [Path("trl/trainer"), Path("trl/experimental")]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pattern")
    parser.add_argument("--context", type=int, default=1)
    args = parser.parse_args()

    found = 0
    for root in ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.py")):
            lines = path.read_text(encoding="utf-8").splitlines()
            matches = [index for index, line in enumerate(lines) if args.pattern in line]
            for index in matches:
                found += 1
                start = max(0, index - args.context)
                end = min(len(lines), index + args.context + 1)
                print(f"\n{path}:{index + 1}")
                for line_number in range(start, end):
                    marker = ">" if line_number == index else " "
                    print(f"{marker} {line_number + 1}: {lines[line_number]}")

    print(f"\nmatches: {found}")
    return 0 if found else 1


if __name__ == "__main__":
    raise SystemExit(main())
