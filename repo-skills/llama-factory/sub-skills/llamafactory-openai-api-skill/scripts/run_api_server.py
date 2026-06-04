#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

from common import env_for


def main() -> int:
    parser = argparse.ArgumentParser(description="Start a LLaMA-Factory OpenAI-compatible API server.")
    parser.add_argument("--work-dir", type=Path, default=Path.cwd(), help="Working directory for logs and relative config paths.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--api-model-name", default="llamafactory-local")
    parser.add_argument("--log", type=Path, default=None)
    parser.add_argument("--pid-file", type=Path, default=None)
    parser.add_argument("--startup-check-seconds", type=float, default=5.0)
    parser.add_argument("--extra-pythonpath", action="append", default=[])
    parser.add_argument("--disable-version-check", action="store_true")
    args = parser.parse_args()

    env = env_for(None, extra_pythonpath=args.extra_pythonpath)
    env["API_HOST"] = args.host
    env["API_PORT"] = str(args.port)
    env["API_MODEL_NAME"] = args.api_model_name
    if args.api_key:
        env["API_KEY"] = args.api_key
    if args.disable_version_check:
        env["DISABLE_VERSION_CHECK"] = "1"
    env["PYTHONUNBUFFERED"] = "1"
    if os.environ.get("CUDA_VISIBLE_DEVICES") is not None:
        env["CUDA_VISIBLE_DEVICES"] = os.environ["CUDA_VISIBLE_DEVICES"]

    cmd = [args.python, "-m", "llamafactory.cli", "api", str(args.config)]
    print("+ " + " ".join(cmd), flush=True)
    log_handle = None
    stdout = None
    if args.log:
        args.log.parent.mkdir(parents=True, exist_ok=True)
        log_handle = args.log.open("a", encoding="utf-8")
        log_handle.write("+ " + " ".join(cmd) + "\n")
        stdout = log_handle
    proc = subprocess.Popen(
        cmd,
        cwd=str(args.work_dir),
        env=env,
        stdout=stdout,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )
    print(f"pid: {proc.pid}")
    if log_handle:
        log_handle.flush()
        log_handle.close()

    deadline = time.time() + args.startup_check_seconds
    while time.time() < deadline:
        code = proc.poll()
        if code is not None:
            print(f"server exited during startup with code {code}")
            if args.log:
                print(f"log: {args.log}")
            return code or 1
        time.sleep(0.5)

    if args.pid_file:
        args.pid_file.parent.mkdir(parents=True, exist_ok=True)
        args.pid_file.write_text(str(proc.pid) + "\n", encoding="utf-8")
    return 0



if __name__ == "__main__":
    raise SystemExit(main())
