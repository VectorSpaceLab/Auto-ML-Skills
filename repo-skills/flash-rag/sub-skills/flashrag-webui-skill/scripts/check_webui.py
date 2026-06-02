#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--timeout", type=float, default=60)
    args = parser.parse_args()
    deadline = time.time() + args.timeout
    last = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(args.url, timeout=5) as resp:
                print(f"status: {resp.status}")
                ok = 200 <= resp.status < 500
                print(f"valid: {str(ok).lower()}")
                return 0 if ok else 1
        except Exception as exc:
            last = exc
            time.sleep(2)
    print("valid: false")
    print(f"- last_error: {type(last).__name__}: {last}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
