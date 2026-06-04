#!/usr/bin/env python
"""Print signatures for important installed TRL public objects.

Use this before writing version-sensitive code. The script has no network or
training side effects.

Example:
    python scripts/inspect_public_api.py
    python scripts/inspect_public_api.py --objects SFTTrainer SFTConfig GRPOConfig
"""

from __future__ import annotations

import argparse
import inspect
import textwrap


DEFAULT_OBJECTS = [
    "SFTTrainer",
    "SFTConfig",
    "DPOTrainer",
    "DPOConfig",
    "GRPOTrainer",
    "GRPOConfig",
    "RLOOTrainer",
    "RLOOConfig",
    "RewardTrainer",
    "RewardConfig",
    "ModelConfig",
    "ScriptArguments",
    "DatasetMixtureConfig",
    "TrlParser",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--objects", nargs="*", default=DEFAULT_OBJECTS, help="Top-level trl objects to inspect.")
    parser.add_argument("--doc", action="store_true", help="Also print the first paragraph of each docstring.")
    args = parser.parse_args()

    import trl

    print(f"trl version: {getattr(trl, '__version__', 'unknown')}")
    for name in args.objects:
        if not hasattr(trl, name):
            print(f"\n## {name}\nmissing from installed trl")
            continue
        obj = getattr(trl, name)
        print(f"\n## {obj.__module__}.{getattr(obj, '__name__', name)}")
        try:
            print(inspect.signature(obj))
        except Exception as exc:
            print(f"signature unavailable: {exc.__class__.__name__}: {exc}")
        if args.doc:
            doc = inspect.getdoc(obj) or ""
            first = doc.split("\n\n", 1)[0]
            if first:
                print(textwrap.shorten(first.replace("\n", " "), width=500))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
