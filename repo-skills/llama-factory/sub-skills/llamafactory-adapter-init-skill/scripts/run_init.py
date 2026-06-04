#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", type=Path, required=True)
    parser.add_argument("--python", default=None)
    parser.add_argument("--log", type=Path, default=None)
    args = parser.parse_args()
    payload = json.loads(args.command.read_text(encoding="utf-8"))
    cmd = list(payload["command"])
    if args.python:
        cmd[0] = args.python
    cwd = Path.cwd()
    env = os.environ.copy()
    print("+ " + " ".join(cmd), flush=True)
    handle = None
    if args.log:
        args.log.parent.mkdir(parents=True, exist_ok=True)
        handle = args.log.open("a", encoding="utf-8")
        handle.write("+ " + " ".join(cmd) + "\n")
    proc = subprocess.Popen(cmd, cwd=str(cwd), env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert proc.stdout is not None
    try:
        for line in proc.stdout:
            print(line, end="")
            if handle:
                handle.write(line)
    finally:
        if handle:
            handle.close()
    return proc.wait()


if __name__ == "__main__":
    raise SystemExit(main())
