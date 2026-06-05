#!/usr/bin/env python3
"""Scan generated skill files for creator-local path leaks."""

import argparse
import pathlib
import re
import sys


DEFAULT_PATTERNS = [
    r"/[^ \n\t]+/source/" + r"sglang",
    r"/[^ \n\t]+/envs/" + r"sglang",
    r"/[^ \n\t]+/model/[^ \n\t]+",
    r"pip" + r" show " + r"Loc" + r"ation",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate that public docs do not contain creator-local paths.")
    parser.add_argument("root", nargs="?", default=".", help="Skill root to scan.")
    parser.add_argument("--pattern", action="append", default=[], help="Extra regex pattern to reject.")
    args = parser.parse_args()

    root = pathlib.Path(args.root).resolve()
    patterns = [re.compile(p) for p in DEFAULT_PATTERNS + args.pattern]
    failures = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in {".md", ".py", ".json", ".yaml", ".yml", ".sh"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pat in patterns:
            if pat.search(text):
                failures.append(f"{path}: matched {pat.pattern}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"ok: no local path leaks under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
