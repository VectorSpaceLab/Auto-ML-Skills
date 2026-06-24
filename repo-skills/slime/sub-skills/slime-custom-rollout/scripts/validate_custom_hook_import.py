#!/usr/bin/env python3
"""Validate importability and basic signature of a slime custom hook."""

from __future__ import annotations

import argparse
import importlib
import inspect


EXPECTED = {
    "rollout": ("args", "rollout_id", "data_source", "evaluation"),
    "custom-generate": ("args", "sample", "sampling_params"),
    "custom-rm-single": ("args", "sample"),
    "custom-rm-group": ("args", "samples"),
    "dynamic-filter": ("args", "samples"),
    "buffer-filter": ("args", "rollout_id", "buffer", "num_samples"),
}


def load(path: str):
    module_name, _, attr = path.rpartition(".")
    if not module_name:
        raise SystemExit("Path must be module.attr")
    return getattr(importlib.import_module(module_name), attr)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True)
    parser.add_argument("--kind", choices=sorted(EXPECTED), required=True)
    args = parser.parse_args()

    fn = load(args.path)
    params = tuple(inspect.signature(fn).parameters)
    expected = EXPECTED[args.kind]
    if params[: len(expected)] != expected:
        raise SystemExit(f"Signature mismatch: got {params}, expected prefix {expected}")
    print(f"OK: {args.path} has signature {inspect.signature(fn)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
