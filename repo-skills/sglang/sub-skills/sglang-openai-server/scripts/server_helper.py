#!/usr/bin/env python3
"""Managed helper for local SGLang server lifecycle."""

import argparse
import json
import os
import pathlib
import signal
import subprocess
import sys
import time
import urllib.request


def pidfile(path):
    return pathlib.Path(path).expanduser().resolve()


def health(url, timeout):
    try:
        with urllib.request.urlopen(url.rstrip("/") + "/health", timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")[:200]
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Start, stop, or check a local SGLang server.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    start = sub.add_parser("start")
    start.add_argument("--model", required=True, help="Model ID/path supplied by the user.")
    start.add_argument("--host", default="127.0.0.1")
    start.add_argument("--port", type=int, default=30000)
    start.add_argument("--pid-file", default=".sglang-server.pid")
    start.add_argument("--log-file", default=".sglang-server.log")
    start.add_argument("--extra-arg", action="append", default=[], help="Additional raw server arg, repeatable.")
    start.add_argument("--wait", type=float, default=0, help="Seconds to wait for /health.")
    stop = sub.add_parser("stop")
    stop.add_argument("--pid-file", default=".sglang-server.pid")
    status = sub.add_parser("status")
    status.add_argument("--base-url", default="http://127.0.0.1:30000")
    args = parser.parse_args()

    if args.cmd == "start":
        pf = pidfile(args.pid_file)
        log = open(args.log_file, "a", encoding="utf-8")
        cmd = [sys.executable, "-m", "sglang.launch_server", "--model-path", args.model, "--host", args.host, "--port", str(args.port)] + args.extra_arg
        proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        pf.write_text(str(proc.pid), encoding="utf-8")
        result = {"pid": proc.pid, "pid_file": str(pf), "log_file": args.log_file, "cmd": cmd}
        if args.wait > 0:
            deadline = time.time() + args.wait
            url = f"http://{args.host}:{args.port}"
            while time.time() < deadline:
                code, body = health(url, 2)
                if code and 200 <= code < 500:
                    result["health"] = {"status": code, "body": body}
                    break
                time.sleep(1)
        print(json.dumps(result, indent=2))
        return 0

    if args.cmd == "stop":
        pf = pidfile(args.pid_file)
        if not pf.exists():
            print(f"no pid file: {pf}")
            return 0
        pid = int(pf.read_text(encoding="utf-8").strip())
        try:
            os.killpg(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        pf.unlink(missing_ok=True)
        print(f"stopped pid group {pid}")
        return 0

    code, body = health(args.base_url, 5)
    print(json.dumps({"base_url": args.base_url, "status": code, "body": body}, indent=2))
    return 0 if code else 1


if __name__ == "__main__":
    raise SystemExit(main())
