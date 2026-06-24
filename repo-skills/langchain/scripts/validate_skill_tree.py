#!/usr/bin/env python3
"""Validate the LangChain skill tree structure and public-content constraints."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FORBIDDEN = [
    "/" + "share" + "/" + "project",
    "/" + "tmp" + "/" + "lcskill",
    "site" + "-" + "packages",
    "pip show " + "Location",
    "source /" + "share" + "/" + "project",
    "set" + "vpn" + ".sh",
    "." + "venv",
]


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated frontmatter")
    meta: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta


def validate_links(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    for match in LINK_RE.finditer(text):
        target = match.group(1)
        if target.startswith(("http://", "https://", "#")):
            continue
        rel = target.split("#", 1)[0]
        if not rel:
            continue
        dest = (path.parent / rel).resolve()
        if not str(dest).startswith(str(ROOT.resolve())):
            errors.append(f"{path}: link escapes tree: {target}")
        elif not dest.exists():
            errors.append(f"{path}: missing link target: {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    skill_files = [ROOT / "SKILL.md"] + sorted((ROOT / "sub-skills").glob("*/SKILL.md"))
    for path in skill_files:
        try:
            meta = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(f"{path}: {exc}")
            continue
        name = meta.get("name", "")
        description = meta.get("description", "")
        if not NAME_RE.match(name):
            errors.append(f"{path}: invalid lowercase-hyphen name {name!r}")
        if not (description.startswith('"') and description.endswith('"')):
            errors.append(f"{path}: description must be double quoted")
        if meta.get("disable-model-invocation") != "true":
            errors.append(f"{path}: disable-model-invocation must be true")
        if path.parent.name != "langchain" and path.parent.name != name:
            errors.append(f"{path}: directory name must match frontmatter name")
        errors.extend(validate_links(path))

    for md in sorted(ROOT.rglob("*.md")):
        rel = md.relative_to(ROOT)
        if rel.parts and rel.parts[0] == "evals":
            continue
        text = md.read_text(encoding="utf-8")
        for token in FORBIDDEN:
            if token in text:
                errors.append(f"{md}: forbidden public token {token!r}")
    for py in sorted(ROOT.rglob("*.py")):
        if not py.read_text(encoding="utf-8").startswith("#!/usr/bin/env python3"):
            errors.append(f"{py}: missing portable shebang")
    evals_json = ROOT / "evals" / "evals.json"
    if not evals_json.exists():
        errors.append("missing evals/evals.json")
    else:
        try:
            json.loads(evals_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"evals/evals.json invalid JSON: {exc}")

    result = {"pass": not errors, "errors": errors}
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        if errors:
            print("FAIL")
            for error in errors:
                print(error)
        else:
            print("PASS")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
