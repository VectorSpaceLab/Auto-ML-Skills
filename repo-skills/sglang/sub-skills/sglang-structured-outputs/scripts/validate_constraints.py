#!/usr/bin/env python3
"""Validate constrained decoding options before sending to SGLang."""

import argparse
import json
import re
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SGLang structured output constraint options.")
    parser.add_argument("--json-schema", help="JSON schema string.")
    parser.add_argument("--regex", help="Regex string.")
    parser.add_argument("--ebnf", help="EBNF grammar string.")
    parser.add_argument("--structural-tag", help="Structural tag string; not mutually exclusive with native grammar fields in this checker.")
    args = parser.parse_args()

    issues = []
    grammar_count = sum(x is not None for x in [args.json_schema, args.regex, args.ebnf])
    if grammar_count > 1:
        issues.append("Only one of --json-schema, --regex, or --ebnf may be set.")
    if args.json_schema:
        try:
            parsed = json.loads(args.json_schema)
            if not isinstance(parsed, dict):
                issues.append("JSON schema must decode to an object.")
        except Exception as exc:
            issues.append(f"invalid JSON schema: {exc}")
    if args.regex:
        try:
            re.compile(args.regex)
        except Exception as exc:
            issues.append(f"invalid regex: {exc}")
    print(json.dumps({"ok": not issues, "issues": issues}, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
