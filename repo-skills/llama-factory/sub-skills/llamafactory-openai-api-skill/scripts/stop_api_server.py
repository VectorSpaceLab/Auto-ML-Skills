#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import signal
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Stop a LLaMA-Factory API server started by run_api_server.py.")
    parser.add_argument("--pid-file", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args()
    if not args.pid_file.is_file():
        print("pid file not found")
        return 0
    pid = int(args.pid_file.read_text(encoding="utf-8").strip())
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        args.pid_file.unlink(missing_ok=True)
        print(f"pid {pid} already stopped")
        return 0
    deadline = time.time() + args.timeout
    while time.time() < deadline:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            args.pid_file.unlink(missing_ok=True)
            print(f"stopped pid {pid}")
            return 0
        time.sleep(0.5)
    try:
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    args.pid_file.unlink(missing_ok=True)
    print(f"killed pid {pid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
