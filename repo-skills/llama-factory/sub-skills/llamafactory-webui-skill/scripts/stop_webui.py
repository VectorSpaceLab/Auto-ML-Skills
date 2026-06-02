#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import signal
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pid-file", type=Path, required=True)
    args = parser.parse_args()
    if not args.pid_file.exists():
        print("valid: true")
        print("- pid file already absent")
        return 0
    pid = int(args.pid_file.read_text(encoding="utf-8").strip())
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"stopped: {pid}")
    except ProcessLookupError:
        print(f"not_running: {pid}")
    args.pid_file.unlink(missing_ok=True)
    print("valid: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
