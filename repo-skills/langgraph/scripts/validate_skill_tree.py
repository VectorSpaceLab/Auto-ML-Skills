#!/usr/bin/env python3
"""Validate LangGraph skill frontmatter, links, paths, and local-path leakage."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SEP = chr(47)
LOCAL_PATH_PATTERNS = [
    re.compile(re.escape(SEP + "share" + SEP)),
    re.compile(re.escape(SEP + "tmp" + SEP)),
    re.compile(re.escape(SEP + "home" + SEP)),
    re.compile(re.escape(SEP + "root" + SEP)),
    re.compile("site" + chr(45) + "packages"),
    re.compile("pip show" + " Location", re.IGNORECASE),
    re.compile(re.escape("source" + SEP + "langgraph")),
]


def is_public_file(path: Path) -> bool:
    return "/evals/" not in path.as_posix()


def check_frontmatter(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if not text.startswith("---\n"):
        return [f"{path}: missing frontmatter"]
    end = text.find("\n---\n", 4)
    if end == -1:
        return [f"{path}: unterminated frontmatter"]
    fm = text[4:end]
    name = re.search(r"^name:\s*([a-z0-9-]+)\s*$", fm, re.MULTILINE)
    desc = re.search(r'^description:\s*"[^"]+"\s*$', fm, re.MULTILINE)
    disable = re.search(
        r"^disable-model-invocation:\s*true\s*$", fm, re.MULTILINE
    )
    if not name:
        errors.append(f"{path}: name must be lowercase-hyphen")
    if not desc:
        errors.append(f"{path}: description must be double-quoted")
    if not disable:
        errors.append(f"{path}: disable-model-invocation must be true")
    return errors


def check_links(path: Path, root: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1)
        if "://" in target or target.startswith("#"):
            continue
        rel = target.split("#", 1)[0]
        if not rel:
            continue
        if not (path.parent / rel).resolve().exists():
            errors.append(f"{path}: broken link {target}")
    return errors


def check_leaks(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if is_public_file(path):
        for pattern in LOCAL_PATH_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path}: possible local-path leak: {pattern.pattern}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []
    for path in sorted(root.rglob("SKILL.md")):
        errors.extend(check_frontmatter(path))
    for path in sorted(root.rglob("*.md")):
        errors.extend(check_links(path, root))
        errors.extend(check_leaks(path))
    for path in sorted(root.rglob("*.py")):
        errors.extend(check_leaks(path))
    for directory in [root / "sub-skills", root / "references", root / "scripts"]:
        if not directory.is_dir():
            errors.append(f"missing directory: {directory}")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"valid: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
