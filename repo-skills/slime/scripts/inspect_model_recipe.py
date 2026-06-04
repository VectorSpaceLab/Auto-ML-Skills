#!/usr/bin/env python3
"""Print bundled Megatron model argument recipes.

The static recipes live in model_recipes.json so future agents can use common
slime model argument blocks without depending on the original source checkout.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_recipes() -> dict[str, list[str]]:
    data_path = Path(__file__).with_name("model_recipes.json")
    try:
        data = json.loads(data_path.read_text())
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing bundled recipe data: {data_path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid bundled recipe data: {data_path}: {exc}") from exc

    recipes = data.get("recipes")
    if not isinstance(recipes, dict):
        raise SystemExit(f"Bundled recipe data has no `recipes` mapping: {data_path}")

    normalized: dict[str, list[str]] = {}
    for key, value in recipes.items():
        if not isinstance(key, str) or not isinstance(value, list) or not all(isinstance(x, str) for x in value):
            raise SystemExit(f"Invalid recipe entry in {data_path}: {key!r}")
        normalized[key.lower()] = value
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect bundled slime model recipe args.")
    parser.add_argument("name", nargs="?", help="Recipe name.")
    parser.add_argument("--list", action="store_true", help="List available recipes.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of shell args.")
    args = parser.parse_args()
    recipes = load_recipes()

    if args.list or not args.name:
        print("\n".join(sorted(recipes)))
        return 0 if args.list else 2

    key = args.name.lower()
    if key not in recipes:
        raise SystemExit(f"Unknown recipe {args.name!r}. Use --list.")

    if args.json:
        print(json.dumps(recipes[key], indent=2))
    else:
        print(" ".join(recipes[key]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
