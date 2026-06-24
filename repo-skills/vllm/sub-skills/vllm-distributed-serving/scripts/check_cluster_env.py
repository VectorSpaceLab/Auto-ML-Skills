#!/usr/bin/env python3
"""Check distributed-serving environment signals without launching a cluster."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = {
        "ray_installed": importlib.util.find_spec("ray") is not None,
        "env": {k: os.environ.get(k) for k in ["CUDA_VISIBLE_DEVICES", "NCCL_SOCKET_IFNAME", "NCCL_DEBUG", "RAY_ADDRESS"] if os.environ.get(k)},
    }
    text = json.dumps(report, indent=2)
    print(text)


if __name__ == "__main__":
    main()
