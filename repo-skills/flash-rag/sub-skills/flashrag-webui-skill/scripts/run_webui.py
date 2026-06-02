#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import env_for


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-dir", type=Path, default=Path.cwd())
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default="7861")
    parser.add_argument("--pid-file", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    args = parser.parse_args()
    env = env_for(None)
    env["GRADIO_SERVER_NAME"] = args.host
    env["GRADIO_SERVER_PORT"] = args.port
    args.log.parent.mkdir(parents=True, exist_ok=True)
    handle = args.log.open("a", encoding="utf-8")
    proc = subprocess.Popen([args.python, "-m", "webui.interface"], cwd=str(args.work_dir), env=env, stdout=handle, stderr=subprocess.STDOUT)
    args.pid_file.parent.mkdir(parents=True, exist_ok=True)
    args.pid_file.write_text(str(proc.pid) + "\n", encoding="utf-8")
    print(f"pid: {proc.pid}")
    print(f"url: http://{args.host}:{args.port}")
    print(f"log: {args.log}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
