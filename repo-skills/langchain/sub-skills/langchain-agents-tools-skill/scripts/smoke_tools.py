#!/usr/bin/env python3
"""No-key smoke test for LangChain tools and agent import."""

from __future__ import annotations

import argparse
import importlib
import json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-agent-import", action="store_true", help="Also import langchain.agents.create_agent.")
    args = parser.parse_args()

    from langchain_core.tools import tool

    @tool
    def add(a: int, b: int) -> int:
        """Add two integers."""
        return a + b

    value = add.invoke({"a": 2, "b": 3})
    schema = add.args_schema.model_json_schema() if add.args_schema else {}
    create_agent_importable = None
    if args.check_agent_import:
        try:
            module = importlib.import_module("langchain.agents")
            create_agent_importable = hasattr(module, "create_agent")
        except Exception:
            create_agent_importable = False
    result = {
        "tool_name": add.name,
        "value": value,
        "schema_has_a": "a" in schema.get("properties", {}),
        "create_agent_importable": create_agent_importable,
    }
    result["pass"] = value == 5 and result["schema_has_a"]
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
