#!/usr/bin/env python3
"""Validate OpenAI tool definitions for common mistakes."""

import argparse
import json
import re


NAME_RE = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a JSON file containing OpenAI tools.")
    parser.add_argument("json_file", nargs="?")
    args = parser.parse_args()
    if not args.json_file:
        print("Provide a JSON file with tools or a full request payload.")
        return 0
    data = json.load(open(args.json_file, encoding="utf-8"))
    tools = data.get("tools", data)
    issues = []
    if not isinstance(tools, list):
        issues.append("tools must be a list")
    else:
        for i, tool in enumerate(tools):
            if tool.get("type") != "function":
                issues.append(f"tool {i} type should be function")
            fn = tool.get("function", {})
            name = fn.get("name")
            if not name or not NAME_RE.match(name):
                issues.append(f"tool {i} invalid function.name")
            params = fn.get("parameters")
            if not isinstance(params, dict) or params.get("type") != "object":
                issues.append(f"tool {i} parameters should be an object JSON schema")
    print(json.dumps({"ok": not issues, "issues": issues}, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
